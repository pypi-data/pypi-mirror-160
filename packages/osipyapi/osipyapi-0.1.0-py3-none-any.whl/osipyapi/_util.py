import asyncio
import hashlib
import math
import multiprocessing
from collections import deque
from datetime import datetime, timedelta
from typing import Deque, Dict, Generator, List, Sequence, Tuple

import polars as pl
from dateutil.tz import tzutc
from dateutil.tz.tz import _tzinfo

from ._enums import BatchDataType, BatchReturnType
from ._exceptions import RequestsDone
from ._types import JSONType



def to_utc(dt: datetime, tz: _tzinfo):
    if not dt.tzinfo:
        return dt.replace(tzinfo=tz).astimezone(tzutc()).replace(tzinfo=None)
    else:
        return dt.astimezone(tzutc()).replace(tzinfo=None)


def split_interpolated_range(
    start_time: datetime,
    end_time: datetime,
    interval: timedelta,
    num_streams: int,
    max_items_per_request: int
) -> Tuple[List[datetime], List[datetime]]:
    """
    Split a time range into several discrete time ranges for interpolated data
    requests. This ensures that the `max_items_per_request` is not exceeded
    """
    request_timedelta: timedelta = end_time - start_time
    request_time_range = request_timedelta.total_seconds()
    # with interpolated data we can calculate how many items to expect
    items_requested = math.ceil(request_time_range / interval.total_seconds() * num_streams)
    if items_requested < max_items_per_request:
        return [start_time], [end_time]
    s = start_time
    e = end_time
    dt = math.floor(interval.total_seconds() * max_items_per_request / num_streams)
    return split_range(s, e, dt)


def split_recorded_range(
    start_time: datetime,
    end_time: datetime,
    num_streams: int,
    max_items_per_request: int
) -> Tuple[List[datetime], List[datetime]]:
    """
    Split a time range into several discrete time ranges for recorded data
    requests. This ensures that the `max_items_per_request` is not exceeded
    """
    request_timedelta: timedelta = end_time - start_time
    request_time_range = request_timedelta.total_seconds()
    # we cant know in advance how many items a single request will return for
    # recorded data. To be abundantly safe we assume an average rate of 1 item
    # per second. If this assumption is broken talk to your PI administrator
    # about their compression strategy because something is wrong
    items_requested = math.ceil(request_time_range * num_streams)
    if items_requested < max_items_per_request:
        return [start_time], [end_time]
    s = start_time
    e = end_time
    dt = math.floor(max_items_per_request / num_streams)
    return split_range(s, e, dt)


def split_range(
    s: datetime,
    e: datetime,
    dt: int
) -> Tuple[List[datetime], List[datetime]]:
    """Split a time range into several discrete time ranges given an interval"""
    start_times = []
    end_times = []
    while s < e:
        start_times.append(s)
        # generates next end time at whatever time produces max_rows
        next_timestamp = s + timedelta(seconds=dt)
        if next_timestamp >= e:
            s = e
        else:
            s = next_timestamp
        end_times.append(s)
    return start_times, end_times


def join_frame(
    sub_frames: List[pl.DataFrame],
    start_time: datetime,
    end_time: datetime
) -> pl.DataFrame:
    """Join all sub frames on common timestamp"""
    seed = sub_frames.pop(0).lazy()
    for sub_frame in sub_frames:
        seed = seed.join(sub_frame.lazy(), on='Timestamp', how='outer').unique()
    # the timestamps in frames should be in chronological order therefore
    # we can skip sorting
    return seed.with_column(
        pl.col(
            'Timestamp'
        ).str.strptime(
            pl.Datetime,
            '%Y-%m-%dT%H:%M:%S%.fZ'
        )
    ).collect().filter(
        (pl.col('Timestamp') > start_time) & (pl.col('Timestamp') < end_time)
    )


def build_recorded_frame(
    start_frame: pl.DataFrame,
    end_frame: pl.DataFrame,
    sub_frames: List[pl.DataFrame],
    start_time: datetime,
    end_time: datetime
) -> pl.DataFrame:
    """
    Join all sub frames and then vertically stack the "cap" frames at the
    start and end times
    """
    frame = join_frame(sub_frames, start_time, end_time)
    return start_frame.vstack(frame).vstack(end_frame)


def content_parser() -> Generator[
    None,
    Tuple[List[Tuple[str, int]], List[Dict[str, JSONType]]],
    List[pl.DataFrame]
]:
    """
    Generator for parsing response content from a stream to a polars dataframe.
    This helps with memory efficiency when processing several batches concurrently.
    It allows a batch of responses to be converted directly to dataframes with
    minimal copying of data.

    This generator works off the principal that all requests for a given
    WebId will be fulfilled before moving onto the next WebId. Also, all data
    for a given WebId will be in chronological order. So for example,
    if each stream requires 3 requests to get all data over the time range the
    responses must come sorted by WebId
    >>> [(R1, W1), (R2, W1), (R3, W1), (R1, W2) ... (Rn, Wn)]
    """
    buffer = deque() # holds data for a WebId until the next batch of responses comes through
    frames = list() # holds dataframes containing data for a single WebId
    last_web_id = None # inbetween response batches hold reference to last WebId
    while True:
        try:
            content_index, content = yield
        except RequestsDone:
            # All requests have completed for batch
            if buffer:
                # We buffered data for a WebId because we didnt know if more
                # requests were coming. No more is coming so convert what we
                # have to a sub frame
                frames.append(build_sub_frame(last_web_id, buffer))
            return frames
        if len(content_index) == 1: # all of the content is for a single WebId
            web_id, _ = content_index.pop(0)
            # if we buffered data for different WebId, convert it to a sub frame
            # and buffer data for the current WebId
            if buffer and web_id != last_web_id:
                frames.append(build_sub_frame(last_web_id, buffer))
            buffer.extend(content)
            last_web_id = web_id
        else:
            for i in range(len(content_index)): # content for multiple WebIds
                web_id, last = content_index.pop(0)
                # We most likely buffered the data for the last WebId from the
                # the previous batch so we check the first WebId in the sequence.
                # if it doesnt match we know the last frame was complete
                if i == 0 and web_id != last_web_id and buffer:
                    frames.append(build_sub_frame(last_web_id, buffer))
                if content_index:   # there is more content for a different WebId
                    # get the index for end of the content for this WebId
                    end = content_index[0][1] - last
                    buffer.extend(content[:end])
                    # remove the content, we dont need it anymore
                    del content[:end]
                    frames.append(build_sub_frame(web_id, buffer))
                else:   # this is the last WebId in the sequence
                    # we could be getting more content for this WebId in the
                    # next batch so buffer the content and save a reference
                    # to the last WebId
                    buffer.extend(content)
                    del content
                    last_web_id = web_id


def build_sub_frame(web_id: str, buffer: Deque[Dict[str, JSONType]]) -> pl.DataFrame:
    """
    Loop through all buffered content. All the content is associated to a
    single WebId. Extract the timestamp and value of each item in the sequence
    and convert it to a dataframe
    """
    data = {'Timestamp': [], web_id: []}
    while buffer:
        segment = buffer.popleft()
        if isinstance(segment, dict):   # could be NoneType if error in response
            for item in segment.get('Items', []):
                timestamp = item['Timestamp']
                good = item['Good']
                if not good:
                    value = None
                else:
                    # if a stream item returned an error, the value will be
                    # None and we're not particularly interested in the errors
                    # https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/topics/error-handling.html
                    value = item['Value']
                    if isinstance(value, dict):
                        value = value['Name']
                data['Timestamp'].append(timestamp)
                data[web_id].append(value)
    if not data['Timestamp']:
        # add a dummy timestamp and value so we can still join on the WebId
        data['Timestamp'].append('1996-02-19T17:27:00Z') # ;)
        data[web_id].append(None)
    return pl.DataFrame(data)


def default_workers():
    return max(multiprocessing.cpu_count()//4, 1)


def generate_task_id(
    web_ids: Sequence[str],
    data_type: BatchDataType,
    start_time: datetime,
    end_time: datetime,
    return_type: BatchReturnType,
    timezone: str,
    interval: timedelta
) -> str:
    web_ids = list(web_ids)
    web_ids.sort()
    n_web_ids = ','.join(web_ids)
    n_dtype = str(data_type)
    n_st = start_time.isoformat()
    n_et = end_time.isoformat()
    n_rtype = str(return_type)
    n_timezone = timezone.lower().strip() if timezone else 'local'
    n_interval = str(interval) if interval else 'none'
    task_id_b = ''.join(
        (n_web_ids, n_dtype, n_st, n_et, n_rtype, n_timezone, n_interval)
    ).encode()
    h = hashlib.md5()
    h.update(task_id_b)
    return h.hexdigest()


def release_waiter(waiter: asyncio.Future, _) -> None:
    if not waiter.done():
        waiter.set_result(None)