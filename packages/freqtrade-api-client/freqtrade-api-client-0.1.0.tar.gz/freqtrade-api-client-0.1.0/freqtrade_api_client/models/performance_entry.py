from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="PerformanceEntry")


@attr.s(auto_attribs=True)
class PerformanceEntry:
    """
    Attributes:
        pair (str):
        profit (float):
        profit_ratio (float):
        profit_pct (float):
        profit_abs (float):
        count (int):
    """

    pair: str
    profit: float
    profit_ratio: float
    profit_pct: float
    profit_abs: float
    count: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pair = self.pair
        profit = self.profit
        profit_ratio = self.profit_ratio
        profit_pct = self.profit_pct
        profit_abs = self.profit_abs
        count = self.count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pair": pair,
                "profit": profit,
                "profit_ratio": profit_ratio,
                "profit_pct": profit_pct,
                "profit_abs": profit_abs,
                "count": count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pair = d.pop("pair")

        profit = d.pop("profit")

        profit_ratio = d.pop("profit_ratio")

        profit_pct = d.pop("profit_pct")

        profit_abs = d.pop("profit_abs")

        count = d.pop("count")

        performance_entry = cls(
            pair=pair,
            profit=profit,
            profit_ratio=profit_ratio,
            profit_pct=profit_pct,
            profit_abs=profit_abs,
            count=count,
        )

        performance_entry.additional_properties = d
        return performance_entry

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
