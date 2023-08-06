from enum import Enum


class CandleType(str, Enum):
    SPOT = "spot"
    FUTURES = "futures"
    MARK = "mark"
    INDEX = "index"
    PREMIUMINDEX = "premiumIndex"
    FUNDING_RATE = "funding_rate"

    def __str__(self) -> str:
        return str(self.value)
