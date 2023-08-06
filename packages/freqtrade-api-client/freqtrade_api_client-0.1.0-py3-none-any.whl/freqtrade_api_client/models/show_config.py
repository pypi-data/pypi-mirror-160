from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.order_types import OrderTypes
from ..models.show_config_entry_pricing import ShowConfigEntryPricing
from ..models.show_config_exit_pricing import ShowConfigExitPricing
from ..models.show_config_minimal_roi import ShowConfigMinimalRoi
from ..models.unfilled_timeout import UnfilledTimeout
from ..types import UNSET, Unset

T = TypeVar("T", bound="ShowConfig")


@attr.s(auto_attribs=True)
class ShowConfig:
    """
    Attributes:
        version (str):
        api_version (float):
        dry_run (bool):
        trading_mode (str):
        short_allowed (bool):
        stake_currency (str):
        stake_amount (str):
        stake_currency_decimals (int):
        max_open_trades (int):
        minimal_roi (ShowConfigMinimalRoi):
        timeframe_ms (int):
        timeframe_min (int):
        exchange (str):
        force_entry_enable (bool):
        exit_pricing (ShowConfigExitPricing):
        entry_pricing (ShowConfigEntryPricing):
        bot_name (str):
        state (str):
        runmode (str):
        position_adjustment_enable (bool):
        max_entry_position_adjustment (int):
        strategy_version (Union[Unset, str]):
        available_capital (Union[Unset, float]):
        stoploss (Union[Unset, float]):
        trailing_stop (Union[Unset, bool]):
        trailing_stop_positive (Union[Unset, float]):
        trailing_stop_positive_offset (Union[Unset, float]):
        trailing_only_offset_is_reached (Union[Unset, bool]):
        unfilledtimeout (Union[Unset, UnfilledTimeout]):
        order_types (Union[Unset, OrderTypes]):
        use_custom_stoploss (Union[Unset, bool]):
        timeframe (Union[Unset, str]):
        strategy (Union[Unset, str]):
    """

    version: str
    api_version: float
    dry_run: bool
    trading_mode: str
    short_allowed: bool
    stake_currency: str
    stake_amount: str
    stake_currency_decimals: int
    max_open_trades: int
    minimal_roi: ShowConfigMinimalRoi
    timeframe_ms: int
    timeframe_min: int
    exchange: str
    force_entry_enable: bool
    exit_pricing: ShowConfigExitPricing
    entry_pricing: ShowConfigEntryPricing
    bot_name: str
    state: str
    runmode: str
    position_adjustment_enable: bool
    max_entry_position_adjustment: int
    strategy_version: Union[Unset, str] = UNSET
    available_capital: Union[Unset, float] = UNSET
    stoploss: Union[Unset, float] = UNSET
    trailing_stop: Union[Unset, bool] = UNSET
    trailing_stop_positive: Union[Unset, float] = UNSET
    trailing_stop_positive_offset: Union[Unset, float] = UNSET
    trailing_only_offset_is_reached: Union[Unset, bool] = UNSET
    unfilledtimeout: Union[Unset, UnfilledTimeout] = UNSET
    order_types: Union[Unset, OrderTypes] = UNSET
    use_custom_stoploss: Union[Unset, bool] = UNSET
    timeframe: Union[Unset, str] = UNSET
    strategy: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        version = self.version
        api_version = self.api_version
        dry_run = self.dry_run
        trading_mode = self.trading_mode
        short_allowed = self.short_allowed
        stake_currency = self.stake_currency
        stake_amount = self.stake_amount
        stake_currency_decimals = self.stake_currency_decimals
        max_open_trades = self.max_open_trades
        minimal_roi = self.minimal_roi.to_dict()

        timeframe_ms = self.timeframe_ms
        timeframe_min = self.timeframe_min
        exchange = self.exchange
        force_entry_enable = self.force_entry_enable
        exit_pricing = self.exit_pricing.to_dict()

        entry_pricing = self.entry_pricing.to_dict()

        bot_name = self.bot_name
        state = self.state
        runmode = self.runmode
        position_adjustment_enable = self.position_adjustment_enable
        max_entry_position_adjustment = self.max_entry_position_adjustment
        strategy_version = self.strategy_version
        available_capital = self.available_capital
        stoploss = self.stoploss
        trailing_stop = self.trailing_stop
        trailing_stop_positive = self.trailing_stop_positive
        trailing_stop_positive_offset = self.trailing_stop_positive_offset
        trailing_only_offset_is_reached = self.trailing_only_offset_is_reached
        unfilledtimeout: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.unfilledtimeout, Unset):
            unfilledtimeout = self.unfilledtimeout.to_dict()

        order_types: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.order_types, Unset):
            order_types = self.order_types.to_dict()

        use_custom_stoploss = self.use_custom_stoploss
        timeframe = self.timeframe
        strategy = self.strategy

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "version": version,
                "api_version": api_version,
                "dry_run": dry_run,
                "trading_mode": trading_mode,
                "short_allowed": short_allowed,
                "stake_currency": stake_currency,
                "stake_amount": stake_amount,
                "stake_currency_decimals": stake_currency_decimals,
                "max_open_trades": max_open_trades,
                "minimal_roi": minimal_roi,
                "timeframe_ms": timeframe_ms,
                "timeframe_min": timeframe_min,
                "exchange": exchange,
                "force_entry_enable": force_entry_enable,
                "exit_pricing": exit_pricing,
                "entry_pricing": entry_pricing,
                "bot_name": bot_name,
                "state": state,
                "runmode": runmode,
                "position_adjustment_enable": position_adjustment_enable,
                "max_entry_position_adjustment": max_entry_position_adjustment,
            }
        )
        if strategy_version is not UNSET:
            field_dict["strategy_version"] = strategy_version
        if available_capital is not UNSET:
            field_dict["available_capital"] = available_capital
        if stoploss is not UNSET:
            field_dict["stoploss"] = stoploss
        if trailing_stop is not UNSET:
            field_dict["trailing_stop"] = trailing_stop
        if trailing_stop_positive is not UNSET:
            field_dict["trailing_stop_positive"] = trailing_stop_positive
        if trailing_stop_positive_offset is not UNSET:
            field_dict["trailing_stop_positive_offset"] = trailing_stop_positive_offset
        if trailing_only_offset_is_reached is not UNSET:
            field_dict["trailing_only_offset_is_reached"] = trailing_only_offset_is_reached
        if unfilledtimeout is not UNSET:
            field_dict["unfilledtimeout"] = unfilledtimeout
        if order_types is not UNSET:
            field_dict["order_types"] = order_types
        if use_custom_stoploss is not UNSET:
            field_dict["use_custom_stoploss"] = use_custom_stoploss
        if timeframe is not UNSET:
            field_dict["timeframe"] = timeframe
        if strategy is not UNSET:
            field_dict["strategy"] = strategy

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        version = d.pop("version")

        api_version = d.pop("api_version")

        dry_run = d.pop("dry_run")

        trading_mode = d.pop("trading_mode")

        short_allowed = d.pop("short_allowed")

        stake_currency = d.pop("stake_currency")

        stake_amount = d.pop("stake_amount")

        stake_currency_decimals = d.pop("stake_currency_decimals")

        max_open_trades = d.pop("max_open_trades")

        minimal_roi = ShowConfigMinimalRoi.from_dict(d.pop("minimal_roi"))

        timeframe_ms = d.pop("timeframe_ms")

        timeframe_min = d.pop("timeframe_min")

        exchange = d.pop("exchange")

        force_entry_enable = d.pop("force_entry_enable")

        exit_pricing = ShowConfigExitPricing.from_dict(d.pop("exit_pricing"))

        entry_pricing = ShowConfigEntryPricing.from_dict(d.pop("entry_pricing"))

        bot_name = d.pop("bot_name")

        state = d.pop("state")

        runmode = d.pop("runmode")

        position_adjustment_enable = d.pop("position_adjustment_enable")

        max_entry_position_adjustment = d.pop("max_entry_position_adjustment")

        strategy_version = d.pop("strategy_version", UNSET)

        available_capital = d.pop("available_capital", UNSET)

        stoploss = d.pop("stoploss", UNSET)

        trailing_stop = d.pop("trailing_stop", UNSET)

        trailing_stop_positive = d.pop("trailing_stop_positive", UNSET)

        trailing_stop_positive_offset = d.pop("trailing_stop_positive_offset", UNSET)

        trailing_only_offset_is_reached = d.pop("trailing_only_offset_is_reached", UNSET)

        _unfilledtimeout = d.pop("unfilledtimeout", UNSET)
        unfilledtimeout: Union[Unset, UnfilledTimeout]
        if isinstance(_unfilledtimeout, Unset):
            unfilledtimeout = UNSET
        else:
            unfilledtimeout = UnfilledTimeout.from_dict(_unfilledtimeout)

        _order_types = d.pop("order_types", UNSET)
        order_types: Union[Unset, OrderTypes]
        if isinstance(_order_types, Unset):
            order_types = UNSET
        else:
            order_types = OrderTypes.from_dict(_order_types)

        use_custom_stoploss = d.pop("use_custom_stoploss", UNSET)

        timeframe = d.pop("timeframe", UNSET)

        strategy = d.pop("strategy", UNSET)

        show_config = cls(
            version=version,
            api_version=api_version,
            dry_run=dry_run,
            trading_mode=trading_mode,
            short_allowed=short_allowed,
            stake_currency=stake_currency,
            stake_amount=stake_amount,
            stake_currency_decimals=stake_currency_decimals,
            max_open_trades=max_open_trades,
            minimal_roi=minimal_roi,
            timeframe_ms=timeframe_ms,
            timeframe_min=timeframe_min,
            exchange=exchange,
            force_entry_enable=force_entry_enable,
            exit_pricing=exit_pricing,
            entry_pricing=entry_pricing,
            bot_name=bot_name,
            state=state,
            runmode=runmode,
            position_adjustment_enable=position_adjustment_enable,
            max_entry_position_adjustment=max_entry_position_adjustment,
            strategy_version=strategy_version,
            available_capital=available_capital,
            stoploss=stoploss,
            trailing_stop=trailing_stop,
            trailing_stop_positive=trailing_stop_positive,
            trailing_stop_positive_offset=trailing_stop_positive_offset,
            trailing_only_offset_is_reached=trailing_only_offset_is_reached,
            unfilledtimeout=unfilledtimeout,
            order_types=order_types,
            use_custom_stoploss=use_custom_stoploss,
            timeframe=timeframe,
            strategy=strategy,
        )

        show_config.additional_properties = d
        return show_config

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
