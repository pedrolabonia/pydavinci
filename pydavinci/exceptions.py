from typing import Optional

import pydavinci.logger as log


class ObjectNotFound(BaseException):
    pass


class TimelineNotFound(BaseException):
    def __init__(self, *args: object, extra: Optional[str] = None) -> None:
        self.message = "Couldn't find a valid timeline."
        if extra:
            log.error(extra)

        super().__init__(*args, self.message)
