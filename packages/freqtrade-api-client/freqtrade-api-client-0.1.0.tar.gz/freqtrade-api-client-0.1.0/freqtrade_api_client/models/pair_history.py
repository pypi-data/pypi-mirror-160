import datetime
from typing import Any, Dict, List, Type, TypeVar, cast

import attr
from dateutil.parser import isoparse

T = TypeVar("T", bound="PairHistory")


@attr.s(auto_attribs=True)
class PairHistory:
    """
    Attributes:
        strategy (str):
        pair (str):
        timeframe (str):
        timeframe_ms (int):
        columns (List[str]):
        data (List[Any]):
        length (int):
        buy_signals (int):
        sell_signals (int):
        enter_long_signals (int):
        exit_long_signals (int):
        enter_short_signals (int):
        exit_short_signals (int):
        last_analyzed (datetime.datetime):
        last_analyzed_ts (int):
        data_start_ts (int):
        data_start (str):
        data_stop (str):
        data_stop_ts (int):
    """

    strategy: str
    pair: str
    timeframe: str
    timeframe_ms: int
    columns: List[str]
    data: List[Any]
    length: int
    buy_signals: int
    sell_signals: int
    enter_long_signals: int
    exit_long_signals: int
    enter_short_signals: int
    exit_short_signals: int
    last_analyzed: datetime.datetime
    last_analyzed_ts: int
    data_start_ts: int
    data_start: str
    data_stop: str
    data_stop_ts: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        strategy = self.strategy
        pair = self.pair
        timeframe = self.timeframe
        timeframe_ms = self.timeframe_ms
        columns = self.columns

        data = self.data

        length = self.length
        buy_signals = self.buy_signals
        sell_signals = self.sell_signals
        enter_long_signals = self.enter_long_signals
        exit_long_signals = self.exit_long_signals
        enter_short_signals = self.enter_short_signals
        exit_short_signals = self.exit_short_signals
        last_analyzed = self.last_analyzed.isoformat()

        last_analyzed_ts = self.last_analyzed_ts
        data_start_ts = self.data_start_ts
        data_start = self.data_start
        data_stop = self.data_stop
        data_stop_ts = self.data_stop_ts

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "strategy": strategy,
                "pair": pair,
                "timeframe": timeframe,
                "timeframe_ms": timeframe_ms,
                "columns": columns,
                "data": data,
                "length": length,
                "buy_signals": buy_signals,
                "sell_signals": sell_signals,
                "enter_long_signals": enter_long_signals,
                "exit_long_signals": exit_long_signals,
                "enter_short_signals": enter_short_signals,
                "exit_short_signals": exit_short_signals,
                "last_analyzed": last_analyzed,
                "last_analyzed_ts": last_analyzed_ts,
                "data_start_ts": data_start_ts,
                "data_start": data_start,
                "data_stop": data_stop,
                "data_stop_ts": data_stop_ts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        strategy = d.pop("strategy")

        pair = d.pop("pair")

        timeframe = d.pop("timeframe")

        timeframe_ms = d.pop("timeframe_ms")

        columns = cast(List[str], d.pop("columns"))

        data = cast(List[Any], d.pop("data"))

        length = d.pop("length")

        buy_signals = d.pop("buy_signals")

        sell_signals = d.pop("sell_signals")

        enter_long_signals = d.pop("enter_long_signals")

        exit_long_signals = d.pop("exit_long_signals")

        enter_short_signals = d.pop("enter_short_signals")

        exit_short_signals = d.pop("exit_short_signals")

        last_analyzed = isoparse(d.pop("last_analyzed"))

        last_analyzed_ts = d.pop("last_analyzed_ts")

        data_start_ts = d.pop("data_start_ts")

        data_start = d.pop("data_start")

        data_stop = d.pop("data_stop")

        data_stop_ts = d.pop("data_stop_ts")

        pair_history = cls(
            strategy=strategy,
            pair=pair,
            timeframe=timeframe,
            timeframe_ms=timeframe_ms,
            columns=columns,
            data=data,
            length=length,
            buy_signals=buy_signals,
            sell_signals=sell_signals,
            enter_long_signals=enter_long_signals,
            exit_long_signals=exit_long_signals,
            enter_short_signals=enter_short_signals,
            exit_short_signals=exit_short_signals,
            last_analyzed=last_analyzed,
            last_analyzed_ts=last_analyzed_ts,
            data_start_ts=data_start_ts,
            data_start=data_start,
            data_stop=data_stop,
            data_stop_ts=data_stop_ts,
        )

        pair_history.additional_properties = d
        return pair_history

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
