from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="BacktestHistoryEntry")


@attr.s(auto_attribs=True)
class BacktestHistoryEntry:
    """
    Attributes:
        filename (str):
        strategy (str):
        run_id (str):
        backtest_start_time (int):
    """

    filename: str
    strategy: str
    run_id: str
    backtest_start_time: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        filename = self.filename
        strategy = self.strategy
        run_id = self.run_id
        backtest_start_time = self.backtest_start_time

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "filename": filename,
                "strategy": strategy,
                "run_id": run_id,
                "backtest_start_time": backtest_start_time,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        filename = d.pop("filename")

        strategy = d.pop("strategy")

        run_id = d.pop("run_id")

        backtest_start_time = d.pop("backtest_start_time")

        backtest_history_entry = cls(
            filename=filename,
            strategy=strategy,
            run_id=run_id,
            backtest_start_time=backtest_start_time,
        )

        backtest_history_entry.additional_properties = d
        return backtest_history_entry

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
