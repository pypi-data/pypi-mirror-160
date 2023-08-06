from enum import Enum


class TradingMode(str, Enum):
    SPOT = "spot"
    MARGIN = "margin"
    FUTURES = "futures"

    def __str__(self) -> str:
        return str(self.value)
