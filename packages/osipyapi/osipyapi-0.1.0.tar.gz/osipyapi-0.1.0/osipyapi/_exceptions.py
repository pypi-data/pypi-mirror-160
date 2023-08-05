from typing import List



class OsiPyException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class TaskNotFound(OsiPyException):
    def __init__(self, task_id: str) -> None:
        self.task_id = task_id

    def __str__(self) -> str:
        return f"Task {self.task_id} not found"


class ChannelSubscriptionError(OsiPyException):
    def __init__(self, not_subscribed: List[str]) -> None:
        self.not_subscribed = not_subscribed


class FailedChannels(ChannelSubscriptionError):
    def __str__(self) -> str:
        return (
            "Not all channels started back up correctly. The following WebId's "
            "are now unsubscribed\n{not_subscribed}".format(
                not_subscribed='\n'.join(self.not_subscribed)
            )
        )

class SubscriptionError(ChannelSubscriptionError):
    def __str__(self) -> str:
        return (
            "Could not subscribe to the following WebId's. Either the max number "
            "number of channels was reached or a network issue occurred\n"
            "{not_subscribed}".format(not_subscribed='\n'.join(self.not_subscribed))
        )


class PolarsException(Exception):
    def __init__(self, exc: BaseException) -> None:
        super().__init__(str(exc))


class ReasonError(OsiPyException):
    def __init__(self, exc: BaseException) -> None:
        self.reason = exc
        self.__cause__ = exc


class HttpConnectionError(ReasonError):
    pass


class HttpPoolError(ReasonError):
    pass


class FrameConstructorError(ReasonError):
    pass


class SignalError(OsiPyException):
    def __init__(self) -> None:
        pass


class RequestsDone(SignalError):
    pass