import datetime
from typing import Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

T = TypeVar("T", bound="DailyRecord")


@attr.s(auto_attribs=True)
class DailyRecord:
    """
    Attributes:
        date (datetime.date):
        abs_profit (float):
        rel_profit (float):
        starting_balance (float):
        fiat_value (float):
        trade_count (int):
    """

    date: datetime.date
    abs_profit: float
    rel_profit: float
    starting_balance: float
    fiat_value: float
    trade_count: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        date = self.date.isoformat()
        abs_profit = self.abs_profit
        rel_profit = self.rel_profit
        starting_balance = self.starting_balance
        fiat_value = self.fiat_value
        trade_count = self.trade_count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
                "abs_profit": abs_profit,
                "rel_profit": rel_profit,
                "starting_balance": starting_balance,
                "fiat_value": fiat_value,
                "trade_count": trade_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        date = isoparse(d.pop("date")).date()

        abs_profit = d.pop("abs_profit")

        rel_profit = d.pop("rel_profit")

        starting_balance = d.pop("starting_balance")

        fiat_value = d.pop("fiat_value")

        trade_count = d.pop("trade_count")

        daily_record = cls(
            date=date,
            abs_profit=abs_profit,
            rel_profit=rel_profit,
            starting_balance=starting_balance,
            fiat_value=fiat_value,
            trade_count=trade_count,
        )

        daily_record.additional_properties = d
        return daily_record

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
