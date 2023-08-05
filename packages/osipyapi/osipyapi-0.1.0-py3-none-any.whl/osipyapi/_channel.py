import asyncio
import functools
import logging
from ssl import SSLContext
from types import TracebackType
from typing import (
    Callable,
    Coroutine,
    Dict,
    List,
    Sequence,
    Set,
    Tuple,
    Type,
    Union
)

import orjson
from attrs import define, field
from attrs.validators import gt, instance_of
from uhttp import (
    Auth,
    Headers,
    Origin,
    Request,
    UHttpException,
    URL,
    W11Protocol
)
from uhttp_negotiate import NegotiateAuth

from ._api import pi_web_api
from ._enums import ChannelState
from ._exceptions import FailedChannels, SubscriptionError
from ._types import HeadersLike



@define
class PiChannel:
    """
    Represents a single websocket connection to PI Web API channel endpoint.
    PiChannels should not be created directly. They should be created by a
    ChannelPool

    Parameters
    - queue (asyncio.Queue): the queue to place received messages into
    - failed_callback (Callable[[Exception], None]): a callback if the receive
    task fails unexpectedly (i.e the websocket connection closed unexpectedly)
    - scheme (str): 'http' or 'https'
    - host (str): the domain name for the PI host
    - port (int): an optional port, if None, will default to 80 for http and
    443 for https
    - auth (Auth): a uhttp auth flow to use on requests. Defaults to NegotiateAuth
    - headers (HeadersLike): optional
    headers to add to each request. Note, you can override these headers on a
    request by request basis

    The rest of parameters are passed directly to the W11Protocol instance
    """
    queue: asyncio.Queue
    failed_callback: Callable[[Exception], None]
    scheme: str
    host: str
    port: int = field(default=None)
    auth: Auth = field(factory=NegotiateAuth, validator=instance_of(Auth))
    headers: HeadersLike = field(factory=Headers.default_headers, converter=Headers)
    ssl: SSLContext = field(default=None)
    close_handshake_timeout: Union[int, float] = field(default=5)
    ping_interval: Union[int, float] = field(default=30)
    ping_timeout: Union[int, float] = field(default=30)
    max_buffered_messages: int = field(default=500)
    connect_timeout: Union[int, float, None] = field(default=5)
    flush_timeout: Union[int, float] = field(default=5)
    ssl_handshake_timeout: Union[int, float, None] = field(default=3)
    ssl_shutdown_timeout: Union[int, float, None] = field(default=0.25)
    happy_eyeballs_delay: Union[int, float, None] = field(default=0.1)
    read_buf_limit: int = field(default=2**16)
    write_buf_limit: int = field(default=2**32)
    auto_reconnect: bool = field(default=True)
    max_reconnect_attempts: int = field(default=30)
    backoff_factor: Union[int, float] = field(default=1.618)
    initial_backoff: Union[int, float] = field(default=5)
    max_backoff: Union[int, float] = field(default=30)
    chunk_size: int = field(default=2**16)
    logger: logging.Logger = field(
        factory=lambda: logging.getLogger(__name__),
        validator=instance_of(logging.Logger)
    )
    loop: asyncio.AbstractEventLoop = field(
        factory=asyncio.get_event_loop,
        validator=instance_of(asyncio.AbstractEventLoop)
    )
    _close_task: asyncio.Task = field(default=None, init=False)
    _close_waiter: asyncio.Future = field(default=None, init=False)
    _connection: W11Protocol = field(default=None, init=False)
    _connection_lock: asyncio.Lock = field(factory=asyncio.Lock, init=False)
    _origin: Origin = field(default=None, init=False)
    _ready: asyncio.Event = field(factory=asyncio.Event, init=False)
    _state: ChannelState = field(default=ChannelState.CLOSED, init=False)
    _subscriptions: List[str] = field(factory=list, init=False)

    def __attrs_post_init__(self):
        origin = Origin(self.scheme, self.host, self.port)
        self._connection = W11Protocol(
            origin,
            self.ssl,
            logger=self.logger,
            loop=self.loop,
            max_reconnect_attempts=self.max_reconnect_attempts,
            max_backoff=self.max_backoff,
            close_handshake_timeout=self.close_handshake_timeout,
            ping_interval=self.ping_interval,
            ping_timeout=self.ping_timeout
        )
        self._origin = origin

    @property
    def state(self) -> ChannelState:
        return self._state

    @property
    def subscriptions(self) -> List[str]:
        return self._subscriptions

    async def start(self, web_ids: Sequence[str]) -> None:
        async with self._connection_lock:
            if self._state is not ChannelState.CLOSED:
                raise RuntimeError(
                    f"Cannot start channel in state {self._state.name}"
                )
            self._state = ChannelState.OPENING
            url = pi_web_api.stream_set.get_channel_adhoc(web_ids)
            url = URL(url).copy_with_origin(self._origin)
            request = Request(
                'GET',
                url,
                self.headers
            )
            # the two coros below can raise a UHttpException
            try:
                await self._connection.aconnect()
                await self._connection.ahandshake(request, self.auth)
            except BaseException:
                self._state = ChannelState.CLOSED
                raise
            task = self.loop.create_task(self.recieve_task())
            self._close_task = self.loop.create_task(self.closing_task(task))
            # wait for closing task to start
            await self._ready.wait()
            self._state = ChannelState.OPEN
            self._subscriptions.extend(web_ids)

    async def stop(self) -> None:
        async with self._connection_lock:
            if self._state is ChannelState.CLOSED:
                return
            close_task = self._close_task
            self._close_task = None
            assert close_task is not None and not close_task.done()
            if self._state is ChannelState.CLOSING:
                # wait for connection to close
                return await close_task
            close_waiter = self._close_waiter
            self._close_waiter = None
            assert close_waiter is not None and not close_waiter.done()
            # signal for connection to close
            close_waiter.set_result(None)
            await asyncio.shield(close_task)

    async def recieve_task(self) -> None:
        assert self._connection._ws_state.name == 'OPEN'
        async for raw_message in self._connection:
            try:
                message = orjson.loads(raw_message)
            except orjson.JSONDecodeError as err:
                self.logger.warning("Error parsing content: %r", err)
            else:
                # if queue is bounded, flow control will trickle down to the
                # tcp level
                await self.queue.put(message)

    async def closing_task(self, receive_task: asyncio.Task) -> None:
        waiter = self.loop.create_future()
        self._close_waiter = waiter
        self._ready.set()
        try:
            await asyncio.wait(
                [receive_task, waiter], return_when=asyncio.FIRST_COMPLETED
            )
        except asyncio.CancelledError:
            receive_task.cancel()
            waiter.cancel()
            self._close_waiter = None
            self._subscriptions.clear()
            self._state = ChannelState.CLOSED
            # Websocket protocol's interrupt helper will ensure close frame
            # is sent and transport is closed
            raise
        if waiter.done():
            # stop called
            receive_task.cancel()
            await self.close_channel()
        else:
            # receive task finished, websocket failed (this also means the
            # websocket was unable to reconnect)
            waiter.cancel()
            self._close_waiter = None
            exc = None
            try:
                await receive_task
            except UHttpException as err:   # should only ever be a UHttpException
                exc = err
            except BaseException:
                self.logger.error("Received non UHttpException in channel", exc_info=True)
                exc = err
            await self.close_channel()
            assert exc is not None
            self.loop.call_soon(self.failed_callback, exc)

    async def close_channel(self) -> None:
        self._state = ChannelState.CLOSING
        try:
            await self._connection.aclose()
        finally:
            self._subscriptions.clear()
            self._state = ChannelState.CLOSED
            
        
@define
class ChannelPool:
    """
    Asynchronous channel pool for connecting to PI Web API channels over
    websocket connections

    Parameters
    - queue (asyncio.Queue): the queue to place received messages into
    - failed_callback (Callable[[Exception], None]): a callback if the receive
    task fails unexpectedly (i.e the websocket connection closed unexpectedly)
    - scheme (str): 'http' or 'https'
    - host (str): the domain name for the PI host
    - port (int): an optional port, if None, will default to 80 for http and
    443 for https
    - auth (Auth): a uhttp auth flow to use on requests. Defaults to NegotiateAuth
    - max_connections (int): the maximum number of websocket connections to
    have open at one time
    - max_streams_per_connection: the maximum number of channels to subscribe
    to per connection. This limitation is to safeguard against 413 status errors
    where the HTTP header can get to larger due to a large query string
    - max_queued_messages: the queue size limit for the pool. The flow control
    will trickle all the way down to the TCP level if messages arent consumed
    - headers (HeadersLike): optional
    headers to add to each request. Note, you can override these headers on a
    request by request basis

    The rest of parameters are passed directly to the W11Protocol instance
    """
    scheme: str
    host: str
    port: int = field(default=None)
    failed_callback: Callable[[BaseException], None] = field(default=None)
    auth: Auth = field(factory=NegotiateAuth)
    max_connections: int = field(
        default=50, validator=[instance_of(int), gt(0)])
    max_streams_per_connection: int = field(
        default=50, validator=[instance_of(int), gt(0)])
    max_queued_messages: int = field(
        default=2000, validator=[instance_of(int), gt(100)]
    )
    headers: Union[Dict[str, str], Tuple[str, str], Tuple[bytes, bytes]] = field(
        factory=Headers.default_headers, converter=Headers
    )
    ssl: SSLContext = field(default=None)
    close_handshake_timeout: Union[int, float] = field(default=5)
    ping_interval: Union[int, float] = field(default=30)
    ping_timeout: Union[int, float] = field(default=30)
    max_buffered_messages: int = field(default=500)
    connect_timeout: Union[int, float, None] = field(default=5)
    flush_timeout: Union[int, float] = field(default=5)
    ssl_handshake_timeout: Union[int, float, None] = field(default=3)
    ssl_shutdown_timeout: Union[int, float, None] = field(default=0.25)
    happy_eyeballs_delay: Union[int, float, None] = field(default=0.1)
    read_buf_limit: int = field(default=2**16)
    write_buf_limit: int = field(default=2**32)
    auto_reconnect: bool = field(default=True)
    max_reconnect_attempts: int = field(default=30)
    backoff_factor: Union[int, float] = field(default=1.618)
    initial_backoff: Union[int, float] = field(default=5)
    max_backoff: Union[int, float] = field(default=60)
    chunk_size: int = field(default=2**16)
    logger: logging.Logger = field(
        factory=functools.partial(logging.getLogger, __name__)
    )
    loop: asyncio.AbstractEventLoop = field(factory=asyncio.get_event_loop)
    _channel_factory: Callable[[None], PiChannel] = field(default=None, init=False)
    _origin: Origin = field(default=None, init=False)
    _pool: List[PiChannel] = field(factory=list, init=False)
    _queue: asyncio.Queue = field(default=None, init=False)
    _pool_lock: asyncio.Lock = field(factory=asyncio.Lock, init=False)
    _subscriptions: Set[str] = field(factory=set, init=False)

    def __attrs_post_init__(self) -> None:
        self._origin = Origin(self.scheme, self.host, self.port)
        self._queue = asyncio.Queue(self.max_buffered_messages)
        self._channel_factory = functools.partial(
            PiChannel,
            self._queue,
            self.channel_failed,
            self.scheme,
            self.host,
            self.port,
            self.auth,
            self.headers,
            self.ssl,
            self.close_handshake_timeout,
            self.ping_interval,
            self.ping_timeout,
            self.max_buffered_messages,
            self.connect_timeout,
            self.flush_timeout,
            self.ssl_handshake_timeout,
            self.ssl_shutdown_timeout,
            self.happy_eyeballs_delay,
            self.read_buf_limit,
            self.write_buf_limit,
            self.auto_reconnect,
            self.max_reconnect_attempts,
            self.backoff_factor,
            self.initial_backoff,
            self.max_backoff,
            self.chunk_size,
            self.logger,
            self.loop
        )

    async def subscribe(self, web_ids: Sequence[str]) -> None:
        """
        Subscribe to a set of WebId's to receive continous updates

        Parameters
        - web_ids (Sequence[str]): the WebId's to subscribe to

        Returns
        - None

        Raises
        - MaxChannelsReached: all or some of the WebId's could not be subscribed
        to because the channel limit was reached. The WebId's not subscribed to
        can be accessed from the `not_subscribed` attribute
        - FailedChannels: all or some of the previously subscribed WebId's are
        now not subscribed because the channels associated to them had an error
        when trying to start back up. The WebId's not subscribed to can be
        accessed from the `not_subscribed` attribute
        """
        async with self._pool_lock:
            self.sync_subscriptions()
            if isinstance(web_ids, str):
                web_ids = [web_ids]
            confirm_added = set(web_ids)
            to_add = list(confirm_added - self._subscriptions)
            if to_add:
                to_start, to_stop = self.attempt_to_subscribe(to_add)
            snapshot = set(self._subscriptions)
            await self.start_stop_channels(to_start, to_stop)
            failed = list(snapshot - self._subscriptions)
            # if we have failed subscriptions, the channels did not start back
            # up properly
            if failed:
                failed.extend(to_add)
                raise FailedChannels(failed)
            not_added = confirm_added - self._subscriptions
            if not_added:
                raise SubscriptionError(not_added)

    async def unsubscribe(self, web_ids: Sequence[str]) -> None:
        """
        Unsubscribe to a set of WebId's

        Parameters
        - web_ids (Sequence[str]): the WebId's to subscribe to

        Returns
        - None

        Raises
        - FailedChannels: all or some of the previously subscribed WebId's are
        now not subscribed because the channels associated to them had an error
        when trying to start back up. The WebId's not subscribed to can be
        accessed from the `not_subscribed` attribute
        """
        async with self._pool_lock:
            self.sync_subscriptions()
            dne = set(web_ids) - self._subscriptions
            to_remove = set(web_ids) - dne
            to_start, to_stop = self.attempt_to_unsubscribe(to_remove)
            snapshot = set(self._subscriptions)
            await self.start_stop_channels(to_start, to_stop)
            failed = list(snapshot - self._subscriptions)
            # if we have failed subscriptions, the channels did not start back
            # up properly
            if failed:
                raise FailedChannels(failed)

    async def close(self) -> None:
        async with self._pool_lock:
            await asyncio.gather(*[channel.stop() for channel in self._pool])
            self._pool = list()

    async def start_stop_channels(
        self,
        to_start: List[Coroutine[None, Sequence[str], None]],
        to_stop: List[Coroutine[None, None, None]]
    ) -> None:
        if to_stop:
            await asyncio.gather(*to_stop, return_exceptions=True)
        if to_start:
            await asyncio.gather(*to_start, return_exceptions=True)
        self.sync_subscriptions()

    async def __aiter__(self):
        while True:
            message = await self._queue.get()
            yield message

    def attempt_to_subscribe(
        self,
        to_add: List[str]
    ) -> Tuple[
        List[Coroutine[None, Sequence[str], None]],
        List[Coroutine[None, None, None]]
    ]:
        to_start = []
        to_stop = []
        # check current channels to see if any of them can take on
        # new subscriptions
        for channel in self._pool:
            channel_subs = list(channel.subscriptions)
            if len(channel_subs) <= self.max_streams_per_connection:
                # get number of available subscriptions channel can
                # take on
                available = self.max_streams_per_connection - len(channel_subs)
                if len(to_add) <= available:
                    # channel can take on all the new subscriptions
                    channel_subs.extend(to_add)
                    del to_add[:]
                    to_stop.append(channel.stop())
                    to_start.append(channel.start(channel_subs))
                    return to_start, to_stop
                else:
                    # we cant subscribe to all web_ids on that channel.
                    # subscribe to what we can and move onto the next
                    # channel
                    channel_subs.extend(to_add[:available])
                    del to_add[:available]
                    to_stop.append(channel.stop())
                    to_start.append(channel.start(channel_subs))
        if to_add:
            # we've gone through all our open channels and determined
            # we dont have enough existing channels to subscribe to
            # everything
            while True:
                if len(self._pool) >= self.max_connections:
                    # we've reached the connection cap, we cant subscribe
                    # to anymore
                    return to_start, to_stop
                channel: PiChannel = self._channel_factory()
                self._pool.insert(0, channel)
                channel_subs = list()
                available = self.max_streams_per_connection
                if len(to_add) <= available:
                    channel_subs.extend(to_add)
                    del to_add[:]
                    to_start.append(channel.start(channel_subs))
                    return to_start, to_stop
                else:
                    channel_subs.extend(to_add[:available])
                    del to_add[:available]
                    to_start.append(channel.start(channel_subs))

    def attempt_to_unsubscribe(
        self,
        to_remove: Set[str]
    ) -> Tuple[
        List[Coroutine[None, Sequence[str], None]],
        List[Coroutine[None, None, None]]
    ]:
        to_start = []
        to_stop = []
        for channel in self._pool:
            to_keep = set(channel.subscriptions) - set(to_remove)
            if len(to_keep) != len(channel.subscriptions):
                # we are removing one, many or all subscriptions from this
                # channel
                to_stop.append(channel.stop())
                if to_keep:
                    # this channel will still support some subscriptions
                    to_start.append(channel.start(to_keep))
        return to_start, to_stop

    def channel_failed(self, exc: BaseException) -> None:
        self.sync_subscriptions()
        self.logger.warning("Channel failed: %r", exc)
        if self.failed_callback is not None:
            self.loop.call_soon(self.failed_callback, exc)

    def sync_subscriptions(self) -> None:
        for idx, channel in reversed(list(enumerate(self._pool))):
            if channel.state is ChannelState.CLOSED:
                self._pool.pop(idx)
        for channel in self._pool:
            self._subscriptions.update(channel.subscriptions)

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] = None,
        exc_value: BaseException = None,
        traceback: TracebackType = None,
    ) -> None:
        await self.close()
        