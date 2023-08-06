from typing import AsyncIterable, Dict, List, Tuple, Union

import rfc3986
from uhttp import Headers, URL



HeadersLike = Union[Headers, Dict[str, str], Tuple[str, str], Tuple[bytes, bytes]]
JSONType = Union[str, int, float, bool, List["JSONType"], Dict[str, "JSONType"]]
UrlLike = Union[URL, str, rfc3986.URIReference]
ContentLike = Union[AsyncIterable[bytes], bytes, bytearray, str, JSONType, None]