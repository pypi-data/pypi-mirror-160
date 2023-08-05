import asyncio
import logging
from ssl import SSLContext
from types import TracebackType
from typing import Type, Union

import orjson
import rfc3986
from attrs import define, field
from attrs.validators import instance_of
from uhttp import (
    Auth,
    H11Pool,
    H11PoolResponse,
    Headers,
    Origin,
    Request,
    URL,
    UHttpException
)
from uhttp_negotiate import NegotiateAuth

from ._exceptions import HttpConnectionError, HttpPoolError
from ._models import PiResponse
from ._types import ContentLike, HeadersLike, UrlLike



@define
class PiClient:
    """
    Base HTTP client for making requests to the Pi Web API

    This class is essentially an H11Pool from uhttp except you must specify the
    origin (i.e the PI host) and responses cannot be streamed they are only
    read into memory and the raw bytes response is converted to a JSON response

    Parameters
    - scheme (str): 'http' or 'https'
    - host (str): the domain name for the PI host
    - port (int): an optional port, if None, will default to 80 for http and
    443 for https
    - auth (Auth): a uhttp auth flow to use on requests. Defaults to NegotiateAuth
    - headers (HeadersLike): optional
    headers to add to each request. Note, you can override these headers on a
    request by request basis

    The rest of parameters are passed directly to the H11Pool instance this
    class uses to fulfill requests
    """
    scheme: str
    host: str
    port: int = field(default=None)
    auth: Auth = field(factory=NegotiateAuth, validator=instance_of(Auth))
    headers: HeadersLike = field(factory=Headers.default_headers, converter=Headers)
    max_connections: int = field(default=50)
    ssl: SSLContext = field(default=None)
    keepalive_timeout: Union[int, float, None] = field(default=None)
    acquire_connection_timeout: Union[int, float, None] = field(default=300)
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
    _origin: Origin = field(default=None, init=False)
    _pool: H11Pool = field(default=None, init=False)

    def __attrs_post_init__(self) -> None:
        origin = Origin(self.scheme, self.host, self.port)
        self._pool = H11Pool(
            origin=origin,
            auth=self.auth,
            max_connections=self.max_connections,
            ssl=self.ssl,
            keepalive_timeout=self.keepalive_timeout,
            acquire_connection_timeout=self.acquire_connection_timeout,
            connect_timeout=self.connect_timeout,
            flush_timeout=self.flush_timeout,
            ssl_handshake_timeout=self.ssl_handshake_timeout,
            ssl_shutdown_timeout=self.ssl_shutdown_timeout,
            happy_eyeballs_delay=self.happy_eyeballs_delay,
            read_buf_limit=self.read_buf_limit,
            write_buf_limit=self.write_buf_limit,
            auto_reconnect=self.auto_reconnect,
            max_reconnect_attempts=self.max_reconnect_attempts,
            backoff_factor=self.backoff_factor,
            initial_backoff=self.initial_backoff,
            max_backoff=self.max_backoff,
            chunk_size=self.chunk_size,
            logger=self.logger,
            loop=self.loop
        )
        self._origin = origin

    async def request(
        self,
        method: str,
        url: UrlLike,
        auth: Auth = None,
        headers: HeadersLike = None,
        content: ContentLike = None,
        read_timeout: Union[int, float, None] = 10,
        write_timeout: Union[int, float, None] = 10
    ):
        """
        Make request to PI Web API

        Parameters
        - method (str): the http method for the request
        - url (UrlLike): the target for the request. The origin will be overwritten
        with the clients origin
        - auth (Auth): the auth flow to use for this request
        - headers (HeadersLike): the http headers to use for this request
        - content (ContentLike): data to be sent with POST, PATCH, or PUT request
        - read_timeout (Union[int, float, None]): the time that the connection
        will wait for the next chunk of data from the socket before failing
        - write_timeout (Union[int, float, None]): the time that the connection
        will wait to flush the socket buffer before failing

        Returns
        - PiResponse

        Raises
        - HttpConnectionError: Error in request, the underlying connection is
        closed but the pool is still active
        - HttpPoolError: Uhandled exception in connection pool. This closes the
        client
        """
        request = self.prep_request(
            method,
            url,
            headers,
            content,
            read_timeout,
            write_timeout
        )
        auth = auth or self.auth
        response = await self.make_request(request, auth)
        json_exc = None
        try:
            # consume all the content to release the connection back to the pool
            content = await response.aread()
        except UHttpException as err:
            # the H11PoolResponse object will take care of cleaning up the
            # connection
            raise HttpConnectionError(err)
        except asyncio.CancelledError:
            await self.close()
            raise
        if content:
            try:
                content = orjson.loads(content)
            except orjson.JSONDecodeError as err:
                json_exc = err
        return PiResponse(
            response.h11_response,
            content,
            json_exc
        )

    async def get(
        self,
        url: UrlLike,
        auth: Auth = None,
        headers: HeadersLike = None,
        read_timeout: Union[int, float, None] = 10,
        write_timeout: Union[int, float, None] = 10
    ) -> PiResponse:
        return await self.request(
            'GET',
            url,
            auth,
            headers,
            None,
            read_timeout,
            write_timeout
        )

    async def post(
        self,
        url: UrlLike,
        auth: Auth = None,
        headers: HeadersLike = None,
        content: ContentLike = None,
        read_timeout: Union[int, float, None] = 10,
        write_timeout: Union[int, float, None] = 10
    ) -> PiResponse:
        return await self.request(
            'POST',
            url,
            auth,
            headers,
            content,
            read_timeout,
            write_timeout
        )

    async def put(
        self,
        url: UrlLike,
        auth: Auth = None,
        headers: HeadersLike = None,
        content: ContentLike = None,
        read_timeout: Union[int, float, None] = 10,
        write_timeout: Union[int, float, None] = 10
    ) -> PiResponse:
        return await self.request(
            'PUT',
            url,
            auth,
            headers,
            content,
            read_timeout,
            write_timeout
        )

    async def patch(
        self,
        url: UrlLike,
        auth: Auth = None,
        headers: HeadersLike = None,
        content: ContentLike = None,
        read_timeout: Union[int, float, None] = 10,
        write_timeout: Union[int, float, None] = 10
    ) -> PiResponse:
        return await self.request(
            'PATCH',
            url,
            auth,
            headers,
            content,
            read_timeout,
            write_timeout
        )

    async def delete(
        self,
        url: UrlLike,
        auth: Auth = None,
        headers: HeadersLike = None,
        read_timeout: Union[int, float, None] = 10,
        write_timeout: Union[int, float, None] = 10
    ) -> PiResponse:
        return await self.request(
            'DELETE',
            url,
            auth,
            headers,
            None,
            read_timeout,
            write_timeout
        )

    async def option(
        self,
        url: UrlLike,
        auth: Auth = None,
        headers: HeadersLike = None,
        read_timeout: Union[int, float, None] = 10,
        write_timeout: Union[int, float, None] = 10
    ) -> PiResponse:
        return await self.request(
            'OPTION',
            url,
            auth,
            headers,
            read_timeout,
            write_timeout
        )

    async def close(self) -> None:
        # closing the pool ensures all the connections are closed but
        # executing another request will reopen the pool. The PI client is
        # just a wrapper for the underlying HTTP connection pool
        await self._pool.aclose()

    async def make_request(self, request: Request, auth: Auth) -> H11PoolResponse:
        try:
            return await self._pool.arequest(request, auth)
        except UHttpException as err:
            # the underlying connection in the pool will be closed but we can
            # still use the pool
            raise HttpConnectionError(err)
        except asyncio.CancelledError:
            await self.close()
            raise
        except BaseException as err:
            # other errors really shouldnt occurr, if they do, close the pool
            self.logger.error("Received non UHttpException in channel", exc_info=True)
            await self.close()
            raise HttpPoolError(err)

    def prep_request(
        self,
        method: str,
        url: Union[URL, str, rfc3986.URIReference],
        headers: HeadersLike = None,
        content: ContentLike = None,
        read_timeout: Union[int, float, None] = 10,
        write_timeout: Union[int, float, None] = 10
    ) -> Request:
        url = URL(url).copy_with_origin(self._origin)
        headers = Headers(headers) if headers is not None else self.headers
        timeouts = dict(read=read_timeout, write=write_timeout)
        request = Request(
            method,
            url,
            headers,
            content,
            timeouts
        )
        if request.method.name not in ('POST', 'PATCH', 'PUT') and request.content is not None:
            raise ValueError(f"Cannot send content in a {request.method.name} request")
        return request

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] = None,
        exc_value: BaseException = None,
        traceback: TracebackType = None,
    ) -> None:
        await self.close()