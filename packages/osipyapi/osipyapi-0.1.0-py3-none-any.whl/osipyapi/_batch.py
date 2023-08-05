import asyncio
import concurrent.futures
import functools
import io
from datetime import datetime, timedelta
from types import TracebackType
from typing import (
    Dict,
    List,
    Sequence,
    Set,
    Tuple,
    Type,
    Union
)

import dateutil.tz
import dateutil.tzwin
import orjson
import pandas as pd
import polars as pl
from attrs import define, field
from attrs.validators import instance_of
from polars.exceptions import (
    ArrowError,
    ComputeError,
    DuplicateError,
    NoDataError,
    NotFoundError,
    PanicException,
    SchemaError,
    ShapeError
)
from uhttp import URL, HttpStatusError

from ._api import pi_web_api
from ._client import PiClient
from ._enums import BatchDataType, BatchReturnType
from ._exceptions import (
    FrameConstructorError,
    HttpConnectionError,
    HttpPoolError,
    PolarsException,
    RequestsDone,
    TaskNotFound
)
from ._types import JSONType
from ._util import (
    build_recorded_frame,
    content_parser,
    default_workers,
    generate_task_id,
    join_frame,
    release_waiter,
    split_interpolated_range,
    split_recorded_range,
    to_utc
)



def frame_builder(
    sub_frames: List[pl.DataFrame],
    dtype: BatchDataType,
    rtype: BatchReturnType,
    st_utc: datetime,
    et_utc: datetime,
    start_frame: pl.DataFrame = None,
    end_frame: pl.DataFrame= None
) -> Union[pl.DataFrame, pd.DataFrame, io.BytesIO]:
    try:
        if dtype is BatchDataType.RECORDED:
            frame = build_recorded_frame(
                start_frame,
                end_frame,
                sub_frames,
                st_utc,
                et_utc
            )
        elif dtype is BatchDataType.INTERPOLATED:
            frame = join_frame(sub_frames, st_utc, et_utc)
        if rtype is BatchReturnType.POLARS:
            return frame
        elif rtype is BatchReturnType.PANDAS:
            return frame.to_pandas()
        buffer = io.BytesIO()
        if rtype is BatchReturnType.JSON_IO:
            frame.write_json(buffer)
        elif rtype is BatchReturnType.CSV_IO:
            frame.write_csv(buffer)
        return buffer
    except (
        ArrowError,
        ComputeError,
        DuplicateError,
        NoDataError,
        NotFoundError,
        PanicException,
        SchemaError,
        ShapeError
    ) as err:
        # polars exceptions cannot be pickled so we capture the reason
        # and re-raise an exception that can be pickled
        exc = PolarsException(err)
        raise FrameConstructorError(exc)
    except BaseException as err:
        raise FrameConstructorError(err)


@define
class BatchDataClient:
    """
    Asynchronous batch data processor for interpolated or recorded data

    The batch data client takes an arbitrary number of WebId's associated to
    PI points and returns an M x N dataframe the number of columns is equivalent
    to the number of unique WebId's passed

    Parameters
    - client (PiClient): the http client used to complete requests
    - request_batch_size (int): the number of requests to submit concurrently
    when retrieving data for a batch. A low number is more memory efficient
    but a high number can (but not always) be faster in terms of I/O
    - max_concurrent (int): the max number of batch jobs which can work
    concurrently. You should take caution when adjusting this number. If its
    too high, the python process will consume too much memory on the system.
    If you are retrieving several small batches (< 1 days worth) this number can
    be quite large (20-40 ish depending on your system resources). If you are
    processing large batches (> 10 days) at small data intervals you can
    quickly exhaust the system memory with more than 4-8 batches. It all just
    depends

    Note:
    The BatchDataClient controls concurrency with a semaphore. You can submit
    hundreds of jobs at a time but only `max_concurrent` will be processing
    at a given moment. For this reason you must retrieve the result of the
    job in order to release the semaphore otherwise all pending jobs will hang
    indefinitely
    """
    client: PiClient
    request_batch_size: int = field(default=30, validator=instance_of(int))
    max_concurrent: int = field(
        factory=lambda: default_workers() * 2, validator=instance_of(int)
    )
    _closing: bool = field(default=False, init=False)
    _executor: concurrent.futures.Executor = field(
        factory=lambda: concurrent.futures.ProcessPoolExecutor(
            max_workers=default_workers()
        ),
        init=False
    )
    _interrupt_task: asyncio.Task = field(default=None, init=False)
    _lock: asyncio.Semaphore = field(default=None, init=False)
    _tasks: List[Tuple[str, asyncio.Task]] = field(factory=list, init=False)


    def __attrs_post_init__(self) -> None:
        self._lock = asyncio.Semaphore(self.max_concurrent)

    async def close(self) -> None:
        self._closing = True
        try:
            for _, task in self._tasks:
                task.cancel()
            self._executor.shutdown(cancel_futures=True)
            await self.client.close()
        finally:
            closer = self._interrupt_task
            self._interrupt_task = None
            if closer is not None:
                closer.cancel()

    def submit(
        self,
        web_ids: Sequence[str],
        data_type: str,
        start_time: datetime,
        end_time: datetime = None,
        return_type: str = 'polars',
        timezone: str = None,
        max_items: int = 100000,
        interval: timedelta = None
    ) -> Tuple[str, asyncio.Future]:
        """
        Submit a batch data request job. This method returns a task_id which can
        be used in the `retrieve` coroutine to await the result along with a
        future which will be released when the job completes

        Parameters
        - web_ids (Sequence[str]): the web_ids to collect data for
        - data_type (str): 'interpolated' or 'recorded'
        - start_time (datetime): the start time of the batch
        - end_time (datetime): the end time of the batch
        - return_type (str): 'polars', 'pandas', 'json_io', or 'csv_io'. The
        'io' variants will return BytesIO objects
        - timezone (str): the local timezone to convert timestamps too. PI
        returns all requests in UTC time offset relative to the timezone of the
        local server. Specifying a timezone ensures the timestamps are offset
        appropriately back to local time
        - max_items (int): the maximum number of data points that PI can return
        in a single request. the default for most PI Web API servers is 150,000
        - interval (timedelta): for 'interpolated' data only, specify the interval
        to return interpolated data on

        Returns
        - task_id (str): used to retrieve batch jobs result
        - waiter (asyncio.Future): signals batch job is complete

        Notes
        - 'interpolated' data will always return a value for each WebId at the
        interval specified. The size of these dataframes is deterministic and
        are almost always smaller than their 'recorded' counterparts
        - 'recorded' data is lossless, every recorded value for a PI point will
        be returned and joined on a common timestamp index. These frames can
        get VERY LARGE very quickly. The size tends to grow exponentially with
        the number of points that are added because the timestamps for two
        different points in the same date range hardly ever have collisions
        """
        # order of web_ids must always be maintained from this point on
        web_ids = list(set(web_ids))
        dtype = BatchDataType.get_dtype(data_type)
        rtype = BatchReturnType.get_rtype(return_type)
        tz = dateutil.tz.gettz(timezone) if timezone else dateutil.tzwin.tzwinlocal() # windows only package
        end_time = end_time or datetime.now()
        st_utc = to_utc(start_time, tz)
        et_utc = to_utc(end_time, tz)
        selected_fields = (
            'Items.Timestamp',
            'Items.Good',
            'Items.Value'
        )
        task_id = generate_task_id(
            web_ids,
            dtype,
            st_utc,
            et_utc,
            rtype,
            timezone,
            interval
        )
        if dtype is BatchDataType.INTERPOLATED:
            task = self.client.loop.create_task(
                self.handle_interpolated_streams(
                    web_ids,
                    st_utc,
                    et_utc,
                    rtype,
                    max_items,
                    interval,
                    selected_fields
                )
            )
        elif dtype is BatchDataType.RECORDED:
            task = self.client.loop.create_task(
                self.handle_recorded_streams(
                    web_ids,
                    st_utc,
                    et_utc,
                    rtype,
                    max_items,
                    selected_fields
                )
            )
        waiter = self.client.loop.create_future()
        task.add_done_callback(functools.partial(release_waiter, waiter))
        self._tasks.append((task_id, task))
        
        self._closing = False
        if self._interrupt_task is None or self._interrupt_task.done():
            self._interrupt_task = self.client.loop.create_task(self.interrupt_task())
        
        return task_id, waiter

    async def retrieve(
        self,
        task_id: str
    ) -> Union[pl.DataFrame, pd.DataFrame, io.BytesIO]:
        """Retrieve the result of a submitted batch job"""
        # a consequence of the "retrieve" system is out of order retrieval.
        # This can be good (most of the time) and bad (in very rare cases)
        # The task ID is generated based on MD5 hash. If a collision occurrs,
        # identical task ID's would generated for actually different batches
        # If coro 1 generated task 1 but coro 2 tries to retrieve the result
        # (using the identical task ID), the result that was intended for coro 1
        # would be given to coro 2 (i.e the wrong result). Collisions arent
        # likely though at the quantities we'll be dealing with so I've chosen
        # to ignore it all together. The possibility is there though
        for i, (match, task) in enumerate(self._tasks):
            if task_id == match:
                self._tasks.pop(i)
                try:
                    return await task
                finally:
                    # release the semaphore so the next batch request enqueued
                    # can go
                    self._lock.release()
        raise TaskNotFound(task_id)

    async def handle_interpolated_streams(
        self,
        web_ids: List[str],
        st_utc: datetime,
        et_utc: datetime,
        rtype: BatchReturnType,
        max_items: int,
        interval: timedelta,
        selected_fields: List[str]
    ) -> pd.DataFrame:
        await self._lock.acquire()
        interval = interval or timedelta(seconds=3600)
        start_times, end_times = split_interpolated_range(
            st_utc,
            et_utc,
            interval,
            1,
            max_items
        )
        urls = []
        # this ensures urls are sorted by web_id
        for web_id in web_ids:
            # this always produces urls in chronological order so we dont
            # need to sort our final frame
            for start_time, end_time in zip(start_times, end_times):
                url = pi_web_api.stream.get_interpolated(
                    web_id,
                    start_time=start_time,
                    end_time=end_time,
                    time_zone='UTC',
                    interval=interval,
                    selected_fields=selected_fields
                )
                urls.append((url, web_id))
        sub_frames = await self.get_sub_frames(urls)
        return await self.client.loop.run_in_executor(
            self._executor,
            frame_builder,
            sub_frames,
            BatchDataType.INTERPOLATED,
            rtype,
            st_utc,
            et_utc
        )

    async def handle_recorded_streams(
        self,
        web_ids: Set[str],
        st_utc: datetime,
        et_utc: datetime,
        rtype: BatchReturnType,
        max_items: int,
        selected_fields: List[str]
    ) -> pd.DataFrame:
        await self._lock.acquire()
        start_frame, end_frame = await self.get_cap_frames(
            web_ids,
            st_utc,
            et_utc
        )
        start_times, end_times = split_recorded_range(
            st_utc,
            et_utc,
            1,
            max_items
        )
        urls = []
        # this ensures urls are sorted by web_id
        for web_id in web_ids:
            # this always produces urls in chronological order so we dont
            # need to sort our final frame
            for start_time, end_time in zip(start_times, end_times):
                url = pi_web_api.stream.get_recorded(
                    web_id,
                    start_time=start_time,
                    end_time=end_time,
                    time_zone='UTC',
                    max_count=max_items,
                    selected_fields=selected_fields
                )
                urls.append((url, web_id))
        sub_frames = await self.get_sub_frames(urls)
        return await self.client.loop.run_in_executor(
            self._executor,
            frame_builder,
            sub_frames,
            BatchDataType.RECORDED,
            rtype,
            st_utc,
            et_utc,
            start_frame,
            end_frame
        )

    async def get_sub_frames(self, urls: List[Tuple[URL, str]]) -> List[pl.DataFrame]:
        parser = content_parser()
        parser.__next__()
        while True:
            web_ids = set()
            requests = list()
            content_index = list()
            # rather than execute all requests concurrently, execute them in
            # batches. This helps with memory efficiency and can actually
            # speed up concurrent batch requests (though any single request
            # is still slower)
            for i in range(self.request_batch_size):
                if urls:
                    url, web_id = urls.pop(0)
                    requests.append(url)
                    if web_id not in web_ids:
                        web_ids.add(web_id)
                        # create an index of where each WebId's content starts
                        # and ends
                        content_index.append((web_id, i))
                else:
                    break
            if not requests:
                try:
                    # all requests processed, lets get our frames
                    parser.throw(RequestsDone)
                except StopIteration as err:
                    return err.value
            dispatch = [self.make_request(request) for request in requests]
            content = await asyncio.gather(*dispatch)
            # let the parser convert what we got to DataFrames before getting
            # more data
            parser.send((content_index, content))

    async def get_cap_frames(
        self,
        web_ids: List[str],
        st_utc: datetime,
        et_utc: datetime,
    ) -> Tuple[pl.DataFrame, pl.DataFrame]:
        # the cap frames are the start and end value for a batch. this is
        # only required for recorded data
        cap_frames = []
        selected_fields=['Timestamp', 'Value', 'Good']
        for time in (st_utc, et_utc):
            data = {'Timestamp': [time.isoformat() + 'Z']}
            data.update({web_id: [] for web_id in web_ids})
            urls = [
                pi_web_api.stream.get_recorded_at_time(
                    web_id, time, time_zone='UTC', selected_fields=selected_fields
                ) for web_id in web_ids
            ]
            dispatch = [self.make_request(url) for url in urls]
            contents = await asyncio.gather(*dispatch)
            for web_id, content in zip(web_ids, contents):
                if content:
                    good = content['Good']
                    if not good:
                        value = None
                    else:
                        value = content['Value']
                        if isinstance(value, dict):
                            value = value['Name']
                    data[web_id].append(value)
                else:
                    data[web_id].append(None)
            cap_frames.append(
                pl.DataFrame(data).with_column(
                    pl.col(
                        'Timestamp'
                    ).str.strptime(
                        pl.Datetime,
                        '%Y-%m-%dT%H:%M:%S%.fZ'
                    )
                )
            )
        return cap_frames[0], cap_frames[1]

    async def make_request(self, url: URL) -> Union[Dict[str, JSONType], None]:
        try:
            response = await self.client.get(url)
        except HttpConnectionError:
            # other requests may succeed, and if they dont and an empty frame
            # is produced an EmptyFrameError will be raised
            return None
        except HttpPoolError:
            raise
        else:
            content = response.content
        try:
            response.raise_for_err()
        except (HttpStatusError, orjson.JSONDecodeError):
            return None
        else:
            return content if isinstance(content, dict) else None

    async def interrupt_task(self):
        waiter = self.client.loop.create_future()
        try:
            await waiter
        except asyncio.CancelledError:
            if not self._closing:
                self.client.logger.debug("Closing batch client on interrupt")
                for _, task in self._tasks:
                    task.cancel()
                self._executor.shutdown(cancel_futures=True)
                try:
                    await self.client.close()
                except RuntimeError: # pool closed while request still in flight
                    pass
            raise

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] = None,
        exc_value: BaseException = None,
        traceback: TracebackType = None,
    ) -> None:
        await self.close()