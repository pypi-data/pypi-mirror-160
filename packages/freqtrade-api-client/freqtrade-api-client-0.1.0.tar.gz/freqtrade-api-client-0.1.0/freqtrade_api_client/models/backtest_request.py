from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="BacktestRequest")


@attr.s(auto_attribs=True)
class BacktestRequest:
    """
    Attributes:
        strategy (str):
        enable_protections (bool):
        timeframe (Union[Unset, str]):
        timeframe_detail (Union[Unset, str]):
        timerange (Union[Unset, str]):
        max_open_trades (Union[Unset, int]):
        stake_amount (Union[Unset, str]):
        dry_run_wallet (Union[Unset, float]):
    """

    strategy: str
    enable_protections: bool
    timeframe: Union[Unset, str] = UNSET
    timeframe_detail: Union[Unset, str] = UNSET
    timerange: Union[Unset, str] = UNSET
    max_open_trades: Union[Unset, int] = UNSET
    stake_amount: Union[Unset, str] = UNSET
    dry_run_wallet: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        strategy = self.strategy
        enable_protections = self.enable_protections
        timeframe = self.timeframe
        timeframe_detail = self.timeframe_detail
        timerange = self.timerange
        max_open_trades = self.max_open_trades
        stake_amount = self.stake_amount
        dry_run_wallet = self.dry_run_wallet

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "strategy": strategy,
                "enable_protections": enable_protections,
            }
        )
        if timeframe is not UNSET:
            field_dict["timeframe"] = timeframe
        if timeframe_detail is not UNSET:
            field_dict["timeframe_detail"] = timeframe_detail
        if timerange is not UNSET:
            field_dict["timerange"] = timerange
        if max_open_trades is not UNSET:
            field_dict["max_open_trades"] = max_open_trades
        if stake_amount is not UNSET:
            field_dict["stake_amount"] = stake_amount
        if dry_run_wallet is not UNSET:
            field_dict["dry_run_wallet"] = dry_run_wallet

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        strategy = d.pop("strategy")

        enable_protections = d.pop("enable_protections")

        timeframe = d.pop("timeframe", UNSET)

        timeframe_detail = d.pop("timeframe_detail", UNSET)

        timerange = d.pop("timerange", UNSET)

        max_open_trades = d.pop("max_open_trades", UNSET)

        stake_amount = d.pop("stake_amount", UNSET)

        dry_run_wallet = d.pop("dry_run_wallet", UNSET)

        backtest_request = cls(
            strategy=strategy,
            enable_protections=enable_protections,
            timeframe=timeframe,
            timeframe_detail=timeframe_detail,
            timerange=timerange,
            max_open_trades=max_open_trades,
            stake_amount=stake_amount,
            dry_run_wallet=dry_run_wallet,
        )

        backtest_request.additional_properties = d
        return backtest_request

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
