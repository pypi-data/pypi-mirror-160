from enum import Enum


class GetEventsResponseType(str, Enum):
    OPERATION = "operation"
    LOGGING = "logging"
    LIFECYCLE = "lifecycle"

    def __str__(self) -> str:
        return str(self.value)
