import pydavinci.logger as log


class ObjectNotFound(BaseException):
    pass


class TimelineNotFound(BaseException):
    def __init__(self, *args: object, extra=None) -> None:
        self.message = "Couldn't find a valid timeline."
        super().__init__(*args, self.message)
        log.error(extra)
