from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="Profit")


@attr.s(auto_attribs=True)
class Profit:
    """
    Attributes:
        profit_closed_coin (float):
        profit_closed_percent_mean (float):
        profit_closed_ratio_mean (float):
        profit_closed_percent_sum (float):
        profit_closed_ratio_sum (float):
        profit_closed_percent (float):
        profit_closed_ratio (float):
        profit_closed_fiat (float):
        profit_all_coin (float):
        profit_all_percent_mean (float):
        profit_all_ratio_mean (float):
        profit_all_percent_sum (float):
        profit_all_ratio_sum (float):
        profit_all_percent (float):
        profit_all_ratio (float):
        profit_all_fiat (float):
        trade_count (int):
        closed_trade_count (int):
        first_trade_date (str):
        first_trade_timestamp (int):
        latest_trade_date (str):
        latest_trade_timestamp (int):
        avg_duration (str):
        best_pair (str):
        best_rate (float):
        best_pair_profit_ratio (float):
        winning_trades (int):
        losing_trades (int):
    """

    profit_closed_coin: float
    profit_closed_percent_mean: float
    profit_closed_ratio_mean: float
    profit_closed_percent_sum: float
    profit_closed_ratio_sum: float
    profit_closed_percent: float
    profit_closed_ratio: float
    profit_closed_fiat: float
    profit_all_coin: float
    profit_all_percent_mean: float
    profit_all_ratio_mean: float
    profit_all_percent_sum: float
    profit_all_ratio_sum: float
    profit_all_percent: float
    profit_all_ratio: float
    profit_all_fiat: float
    trade_count: int
    closed_trade_count: int
    first_trade_date: str
    first_trade_timestamp: int
    latest_trade_date: str
    latest_trade_timestamp: int
    avg_duration: str
    best_pair: str
    best_rate: float
    best_pair_profit_ratio: float
    winning_trades: int
    losing_trades: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        profit_closed_coin = self.profit_closed_coin
        profit_closed_percent_mean = self.profit_closed_percent_mean
        profit_closed_ratio_mean = self.profit_closed_ratio_mean
        profit_closed_percent_sum = self.profit_closed_percent_sum
        profit_closed_ratio_sum = self.profit_closed_ratio_sum
        profit_closed_percent = self.profit_closed_percent
        profit_closed_ratio = self.profit_closed_ratio
        profit_closed_fiat = self.profit_closed_fiat
        profit_all_coin = self.profit_all_coin
        profit_all_percent_mean = self.profit_all_percent_mean
        profit_all_ratio_mean = self.profit_all_ratio_mean
        profit_all_percent_sum = self.profit_all_percent_sum
        profit_all_ratio_sum = self.profit_all_ratio_sum
        profit_all_percent = self.profit_all_percent
        profit_all_ratio = self.profit_all_ratio
        profit_all_fiat = self.profit_all_fiat
        trade_count = self.trade_count
        closed_trade_count = self.closed_trade_count
        first_trade_date = self.first_trade_date
        first_trade_timestamp = self.first_trade_timestamp
        latest_trade_date = self.latest_trade_date
        latest_trade_timestamp = self.latest_trade_timestamp
        avg_duration = self.avg_duration
        best_pair = self.best_pair
        best_rate = self.best_rate
        best_pair_profit_ratio = self.best_pair_profit_ratio
        winning_trades = self.winning_trades
        losing_trades = self.losing_trades

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "profit_closed_coin": profit_closed_coin,
                "profit_closed_percent_mean": profit_closed_percent_mean,
                "profit_closed_ratio_mean": profit_closed_ratio_mean,
                "profit_closed_percent_sum": profit_closed_percent_sum,
                "profit_closed_ratio_sum": profit_closed_ratio_sum,
                "profit_closed_percent": profit_closed_percent,
                "profit_closed_ratio": profit_closed_ratio,
                "profit_closed_fiat": profit_closed_fiat,
                "profit_all_coin": profit_all_coin,
                "profit_all_percent_mean": profit_all_percent_mean,
                "profit_all_ratio_mean": profit_all_ratio_mean,
                "profit_all_percent_sum": profit_all_percent_sum,
                "profit_all_ratio_sum": profit_all_ratio_sum,
                "profit_all_percent": profit_all_percent,
                "profit_all_ratio": profit_all_ratio,
                "profit_all_fiat": profit_all_fiat,
                "trade_count": trade_count,
                "closed_trade_count": closed_trade_count,
                "first_trade_date": first_trade_date,
                "first_trade_timestamp": first_trade_timestamp,
                "latest_trade_date": latest_trade_date,
                "latest_trade_timestamp": latest_trade_timestamp,
                "avg_duration": avg_duration,
                "best_pair": best_pair,
                "best_rate": best_rate,
                "best_pair_profit_ratio": best_pair_profit_ratio,
                "winning_trades": winning_trades,
                "losing_trades": losing_trades,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        profit_closed_coin = d.pop("profit_closed_coin")

        profit_closed_percent_mean = d.pop("profit_closed_percent_mean")

        profit_closed_ratio_mean = d.pop("profit_closed_ratio_mean")

        profit_closed_percent_sum = d.pop("profit_closed_percent_sum")

        profit_closed_ratio_sum = d.pop("profit_closed_ratio_sum")

        profit_closed_percent = d.pop("profit_closed_percent")

        profit_closed_ratio = d.pop("profit_closed_ratio")

        profit_closed_fiat = d.pop("profit_closed_fiat")

        profit_all_coin = d.pop("profit_all_coin")

        profit_all_percent_mean = d.pop("profit_all_percent_mean")

        profit_all_ratio_mean = d.pop("profit_all_ratio_mean")

        profit_all_percent_sum = d.pop("profit_all_percent_sum")

        profit_all_ratio_sum = d.pop("profit_all_ratio_sum")

        profit_all_percent = d.pop("profit_all_percent")

        profit_all_ratio = d.pop("profit_all_ratio")

        profit_all_fiat = d.pop("profit_all_fiat")

        trade_count = d.pop("trade_count")

        closed_trade_count = d.pop("closed_trade_count")

        first_trade_date = d.pop("first_trade_date")

        first_trade_timestamp = d.pop("first_trade_timestamp")

        latest_trade_date = d.pop("latest_trade_date")

        latest_trade_timestamp = d.pop("latest_trade_timestamp")

        avg_duration = d.pop("avg_duration")

        best_pair = d.pop("best_pair")

        best_rate = d.pop("best_rate")

        best_pair_profit_ratio = d.pop("best_pair_profit_ratio")

        winning_trades = d.pop("winning_trades")

        losing_trades = d.pop("losing_trades")

        profit = cls(
            profit_closed_coin=profit_closed_coin,
            profit_closed_percent_mean=profit_closed_percent_mean,
            profit_closed_ratio_mean=profit_closed_ratio_mean,
            profit_closed_percent_sum=profit_closed_percent_sum,
            profit_closed_ratio_sum=profit_closed_ratio_sum,
            profit_closed_percent=profit_closed_percent,
            profit_closed_ratio=profit_closed_ratio,
            profit_closed_fiat=profit_closed_fiat,
            profit_all_coin=profit_all_coin,
            profit_all_percent_mean=profit_all_percent_mean,
            profit_all_ratio_mean=profit_all_ratio_mean,
            profit_all_percent_sum=profit_all_percent_sum,
            profit_all_ratio_sum=profit_all_ratio_sum,
            profit_all_percent=profit_all_percent,
            profit_all_ratio=profit_all_ratio,
            profit_all_fiat=profit_all_fiat,
            trade_count=trade_count,
            closed_trade_count=closed_trade_count,
            first_trade_date=first_trade_date,
            first_trade_timestamp=first_trade_timestamp,
            latest_trade_date=latest_trade_date,
            latest_trade_timestamp=latest_trade_timestamp,
            avg_duration=avg_duration,
            best_pair=best_pair,
            best_rate=best_rate,
            best_pair_profit_ratio=best_pair_profit_ratio,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
        )

        profit.additional_properties = d
        return profit

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
