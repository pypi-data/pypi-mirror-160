from enum import Enum


class SignalDirection(str, Enum):
    LONG = "long"
    SHORT = "short"

    def __str__(self) -> str:
        return str(self.value)
