from typing import Union

import orjson
from attrs import frozen
from uhttp import H11Response

from ._types import JSONType



@frozen
class PiResponse:
    response: H11Response
    content: JSONType
    json_exc: Union[orjson.JSONDecodeError, None]

    def raise_for_err(self) -> None:
        self.response.raise_for_status()
        if self.json_exc:
            raise self.json_exc