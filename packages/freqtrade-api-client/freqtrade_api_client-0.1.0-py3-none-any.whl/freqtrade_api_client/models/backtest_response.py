from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.backtest_response_backtest_result import BacktestResponseBacktestResult
from ..types import UNSET, Unset

T = TypeVar("T", bound="BacktestResponse")


@attr.s(auto_attribs=True)
class BacktestResponse:
    """
    Attributes:
        status (str):
        running (bool):
        status_msg (str):
        step (str):
        progress (float):
        trade_count (Union[Unset, float]):
        backtest_result (Union[Unset, BacktestResponseBacktestResult]):
    """

    status: str
    running: bool
    status_msg: str
    step: str
    progress: float
    trade_count: Union[Unset, float] = UNSET
    backtest_result: Union[Unset, BacktestResponseBacktestResult] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status
        running = self.running
        status_msg = self.status_msg
        step = self.step
        progress = self.progress
        trade_count = self.trade_count
        backtest_result: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.backtest_result, Unset):
            backtest_result = self.backtest_result.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "running": running,
                "status_msg": status_msg,
                "step": step,
                "progress": progress,
            }
        )
        if trade_count is not UNSET:
            field_dict["trade_count"] = trade_count
        if backtest_result is not UNSET:
            field_dict["backtest_result"] = backtest_result

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = d.pop("status")

        running = d.pop("running")

        status_msg = d.pop("status_msg")

        step = d.pop("step")

        progress = d.pop("progress")

        trade_count = d.pop("trade_count", UNSET)

        _backtest_result = d.pop("backtest_result", UNSET)
        backtest_result: Union[Unset, BacktestResponseBacktestResult]
        if isinstance(_backtest_result, Unset):
            backtest_result = UNSET
        else:
            backtest_result = BacktestResponseBacktestResult.from_dict(_backtest_result)

        backtest_response = cls(
            status=status,
            running=running,
            status_msg=status_msg,
            step=step,
            progress=progress,
            trade_count=trade_count,
            backtest_result=backtest_result,
        )

        backtest_response.additional_properties = d
        return backtest_response

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
