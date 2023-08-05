import enum



class BatchDataType(str, enum.Enum):
    INTERPOLATED = 'interpolated'
    RECORDED = 'recorded'

    @classmethod
    def get_dtype(cls, dtype: str) -> "BatchDataType":
        return cls(dtype.strip().lower())


class BatchReturnType(str, enum.Enum):
    POLARS = 'polars'
    PANDAS = 'pandas'
    JSON_IO = 'json_io'
    CSV_IO = 'csv_io'

    @classmethod
    def get_rtype(cls, rtype: str) -> "BatchReturnType":
        return cls(rtype.strip().lower())


class ChannelState(enum.IntEnum):
    CLOSED = 0
    CLOSING = 1
    OPENING = 2
    OPEN = 3


class ChannelPoolState(enum.IntEnum):
    CLOSED = 0
    CLOSING = 1
    OPEN = 2