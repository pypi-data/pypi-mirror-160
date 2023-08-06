from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.order_schema import OrderSchema
from ..models.trading_mode import TradingMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="OpenTradeSchema")


@attr.s(auto_attribs=True)
class OpenTradeSchema:
    """
    Attributes:
        trade_id (int):
        pair (str):
        base_currency (str):
        quote_currency (str):
        is_open (bool):
        is_short (bool):
        exchange (str):
        amount (float):
        amount_requested (float):
        stake_amount (float):
        strategy (str):
        timeframe (int):
        open_date (str):
        open_timestamp (int):
        open_rate (float):
        open_trade_value (float):
        orders (List[OrderSchema]):
        current_profit (float):
        current_profit_abs (float):
        current_profit_pct (float):
        current_rate (float):
        buy_tag (Union[Unset, str]):
        enter_tag (Union[Unset, str]):
        fee_open (Union[Unset, float]):
        fee_open_cost (Union[Unset, float]):
        fee_open_currency (Union[Unset, str]):
        fee_close (Union[Unset, float]):
        fee_close_cost (Union[Unset, float]):
        fee_close_currency (Union[Unset, str]):
        open_rate_requested (Union[Unset, float]):
        close_date (Union[Unset, str]):
        close_timestamp (Union[Unset, int]):
        close_rate (Union[Unset, float]):
        close_rate_requested (Union[Unset, float]):
        close_profit (Union[Unset, float]):
        close_profit_pct (Union[Unset, float]):
        close_profit_abs (Union[Unset, float]):
        profit_ratio (Union[Unset, float]):
        profit_pct (Union[Unset, float]):
        profit_abs (Union[Unset, float]):
        profit_fiat (Union[Unset, float]):
        sell_reason (Union[Unset, str]):
        exit_reason (Union[Unset, str]):
        exit_order_status (Union[Unset, str]):
        stop_loss_abs (Union[Unset, float]):
        stop_loss_ratio (Union[Unset, float]):
        stop_loss_pct (Union[Unset, float]):
        stoploss_order_id (Union[Unset, str]):
        stoploss_last_update (Union[Unset, str]):
        stoploss_last_update_timestamp (Union[Unset, int]):
        initial_stop_loss_abs (Union[Unset, float]):
        initial_stop_loss_ratio (Union[Unset, float]):
        initial_stop_loss_pct (Union[Unset, float]):
        min_rate (Union[Unset, float]):
        max_rate (Union[Unset, float]):
        open_order_id (Union[Unset, str]):
        leverage (Union[Unset, float]):
        interest_rate (Union[Unset, float]):
        liquidation_price (Union[Unset, float]):
        funding_fees (Union[Unset, float]):
        trading_mode (Union[Unset, TradingMode]): Enum to distinguish between
            spot, margin, futures or any other trading method
        stoploss_current_dist (Union[Unset, float]):
        stoploss_current_dist_pct (Union[Unset, float]):
        stoploss_current_dist_ratio (Union[Unset, float]):
        stoploss_entry_dist (Union[Unset, float]):
        stoploss_entry_dist_ratio (Union[Unset, float]):
        open_order (Union[Unset, str]):
    """

    trade_id: int
    pair: str
    base_currency: str
    quote_currency: str
    is_open: bool
    is_short: bool
    exchange: str
    amount: float
    amount_requested: float
    stake_amount: float
    strategy: str
    timeframe: int
    open_date: str
    open_timestamp: int
    open_rate: float
    open_trade_value: float
    orders: List[OrderSchema]
    current_profit: float
    current_profit_abs: float
    current_profit_pct: float
    current_rate: float
    buy_tag: Union[Unset, str] = UNSET
    enter_tag: Union[Unset, str] = UNSET
    fee_open: Union[Unset, float] = UNSET
    fee_open_cost: Union[Unset, float] = UNSET
    fee_open_currency: Union[Unset, str] = UNSET
    fee_close: Union[Unset, float] = UNSET
    fee_close_cost: Union[Unset, float] = UNSET
    fee_close_currency: Union[Unset, str] = UNSET
    open_rate_requested: Union[Unset, float] = UNSET
    close_date: Union[Unset, str] = UNSET
    close_timestamp: Union[Unset, int] = UNSET
    close_rate: Union[Unset, float] = UNSET
    close_rate_requested: Union[Unset, float] = UNSET
    close_profit: Union[Unset, float] = UNSET
    close_profit_pct: Union[Unset, float] = UNSET
    close_profit_abs: Union[Unset, float] = UNSET
    profit_ratio: Union[Unset, float] = UNSET
    profit_pct: Union[Unset, float] = UNSET
    profit_abs: Union[Unset, float] = UNSET
    profit_fiat: Union[Unset, float] = UNSET
    sell_reason: Union[Unset, str] = UNSET
    exit_reason: Union[Unset, str] = UNSET
    exit_order_status: Union[Unset, str] = UNSET
    stop_loss_abs: Union[Unset, float] = UNSET
    stop_loss_ratio: Union[Unset, float] = UNSET
    stop_loss_pct: Union[Unset, float] = UNSET
    stoploss_order_id: Union[Unset, str] = UNSET
    stoploss_last_update: Union[Unset, str] = UNSET
    stoploss_last_update_timestamp: Union[Unset, int] = UNSET
    initial_stop_loss_abs: Union[Unset, float] = UNSET
    initial_stop_loss_ratio: Union[Unset, float] = UNSET
    initial_stop_loss_pct: Union[Unset, float] = UNSET
    min_rate: Union[Unset, float] = UNSET
    max_rate: Union[Unset, float] = UNSET
    open_order_id: Union[Unset, str] = UNSET
    leverage: Union[Unset, float] = UNSET
    interest_rate: Union[Unset, float] = UNSET
    liquidation_price: Union[Unset, float] = UNSET
    funding_fees: Union[Unset, float] = UNSET
    trading_mode: Union[Unset, TradingMode] = UNSET
    stoploss_current_dist: Union[Unset, float] = UNSET
    stoploss_current_dist_pct: Union[Unset, float] = UNSET
    stoploss_current_dist_ratio: Union[Unset, float] = UNSET
    stoploss_entry_dist: Union[Unset, float] = UNSET
    stoploss_entry_dist_ratio: Union[Unset, float] = UNSET
    open_order: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trade_id = self.trade_id
        pair = self.pair
        base_currency = self.base_currency
        quote_currency = self.quote_currency
        is_open = self.is_open
        is_short = self.is_short
        exchange = self.exchange
        amount = self.amount
        amount_requested = self.amount_requested
        stake_amount = self.stake_amount
        strategy = self.strategy
        timeframe = self.timeframe
        open_date = self.open_date
        open_timestamp = self.open_timestamp
        open_rate = self.open_rate
        open_trade_value = self.open_trade_value
        orders = []
        for orders_item_data in self.orders:
            orders_item = orders_item_data.to_dict()

            orders.append(orders_item)

        current_profit = self.current_profit
        current_profit_abs = self.current_profit_abs
        current_profit_pct = self.current_profit_pct
        current_rate = self.current_rate
        buy_tag = self.buy_tag
        enter_tag = self.enter_tag
        fee_open = self.fee_open
        fee_open_cost = self.fee_open_cost
        fee_open_currency = self.fee_open_currency
        fee_close = self.fee_close
        fee_close_cost = self.fee_close_cost
        fee_close_currency = self.fee_close_currency
        open_rate_requested = self.open_rate_requested
        close_date = self.close_date
        close_timestamp = self.close_timestamp
        close_rate = self.close_rate
        close_rate_requested = self.close_rate_requested
        close_profit = self.close_profit
        close_profit_pct = self.close_profit_pct
        close_profit_abs = self.close_profit_abs
        profit_ratio = self.profit_ratio
        profit_pct = self.profit_pct
        profit_abs = self.profit_abs
        profit_fiat = self.profit_fiat
        sell_reason = self.sell_reason
        exit_reason = self.exit_reason
        exit_order_status = self.exit_order_status
        stop_loss_abs = self.stop_loss_abs
        stop_loss_ratio = self.stop_loss_ratio
        stop_loss_pct = self.stop_loss_pct
        stoploss_order_id = self.stoploss_order_id
        stoploss_last_update = self.stoploss_last_update
        stoploss_last_update_timestamp = self.stoploss_last_update_timestamp
        initial_stop_loss_abs = self.initial_stop_loss_abs
        initial_stop_loss_ratio = self.initial_stop_loss_ratio
        initial_stop_loss_pct = self.initial_stop_loss_pct
        min_rate = self.min_rate
        max_rate = self.max_rate
        open_order_id = self.open_order_id
        leverage = self.leverage
        interest_rate = self.interest_rate
        liquidation_price = self.liquidation_price
        funding_fees = self.funding_fees
        trading_mode: Union[Unset, str] = UNSET
        if not isinstance(self.trading_mode, Unset):
            trading_mode = self.trading_mode.value

        stoploss_current_dist = self.stoploss_current_dist
        stoploss_current_dist_pct = self.stoploss_current_dist_pct
        stoploss_current_dist_ratio = self.stoploss_current_dist_ratio
        stoploss_entry_dist = self.stoploss_entry_dist
        stoploss_entry_dist_ratio = self.stoploss_entry_dist_ratio
        open_order = self.open_order

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "trade_id": trade_id,
                "pair": pair,
                "base_currency": base_currency,
                "quote_currency": quote_currency,
                "is_open": is_open,
                "is_short": is_short,
                "exchange": exchange,
                "amount": amount,
                "amount_requested": amount_requested,
                "stake_amount": stake_amount,
                "strategy": strategy,
                "timeframe": timeframe,
                "open_date": open_date,
                "open_timestamp": open_timestamp,
                "open_rate": open_rate,
                "open_trade_value": open_trade_value,
                "orders": orders,
                "current_profit": current_profit,
                "current_profit_abs": current_profit_abs,
                "current_profit_pct": current_profit_pct,
                "current_rate": current_rate,
            }
        )
        if buy_tag is not UNSET:
            field_dict["buy_tag"] = buy_tag
        if enter_tag is not UNSET:
            field_dict["enter_tag"] = enter_tag
        if fee_open is not UNSET:
            field_dict["fee_open"] = fee_open
        if fee_open_cost is not UNSET:
            field_dict["fee_open_cost"] = fee_open_cost
        if fee_open_currency is not UNSET:
            field_dict["fee_open_currency"] = fee_open_currency
        if fee_close is not UNSET:
            field_dict["fee_close"] = fee_close
        if fee_close_cost is not UNSET:
            field_dict["fee_close_cost"] = fee_close_cost
        if fee_close_currency is not UNSET:
            field_dict["fee_close_currency"] = fee_close_currency
        if open_rate_requested is not UNSET:
            field_dict["open_rate_requested"] = open_rate_requested
        if close_date is not UNSET:
            field_dict["close_date"] = close_date
        if close_timestamp is not UNSET:
            field_dict["close_timestamp"] = close_timestamp
        if close_rate is not UNSET:
            field_dict["close_rate"] = close_rate
        if close_rate_requested is not UNSET:
            field_dict["close_rate_requested"] = close_rate_requested
        if close_profit is not UNSET:
            field_dict["close_profit"] = close_profit
        if close_profit_pct is not UNSET:
            field_dict["close_profit_pct"] = close_profit_pct
        if close_profit_abs is not UNSET:
            field_dict["close_profit_abs"] = close_profit_abs
        if profit_ratio is not UNSET:
            field_dict["profit_ratio"] = profit_ratio
        if profit_pct is not UNSET:
            field_dict["profit_pct"] = profit_pct
        if profit_abs is not UNSET:
            field_dict["profit_abs"] = profit_abs
        if profit_fiat is not UNSET:
            field_dict["profit_fiat"] = profit_fiat
        if sell_reason is not UNSET:
            field_dict["sell_reason"] = sell_reason
        if exit_reason is not UNSET:
            field_dict["exit_reason"] = exit_reason
        if exit_order_status is not UNSET:
            field_dict["exit_order_status"] = exit_order_status
        if stop_loss_abs is not UNSET:
            field_dict["stop_loss_abs"] = stop_loss_abs
        if stop_loss_ratio is not UNSET:
            field_dict["stop_loss_ratio"] = stop_loss_ratio
        if stop_loss_pct is not UNSET:
            field_dict["stop_loss_pct"] = stop_loss_pct
        if stoploss_order_id is not UNSET:
            field_dict["stoploss_order_id"] = stoploss_order_id
        if stoploss_last_update is not UNSET:
            field_dict["stoploss_last_update"] = stoploss_last_update
        if stoploss_last_update_timestamp is not UNSET:
            field_dict["stoploss_last_update_timestamp"] = stoploss_last_update_timestamp
        if initial_stop_loss_abs is not UNSET:
            field_dict["initial_stop_loss_abs"] = initial_stop_loss_abs
        if initial_stop_loss_ratio is not UNSET:
            field_dict["initial_stop_loss_ratio"] = initial_stop_loss_ratio
        if initial_stop_loss_pct is not UNSET:
            field_dict["initial_stop_loss_pct"] = initial_stop_loss_pct
        if min_rate is not UNSET:
            field_dict["min_rate"] = min_rate
        if max_rate is not UNSET:
            field_dict["max_rate"] = max_rate
        if open_order_id is not UNSET:
            field_dict["open_order_id"] = open_order_id
        if leverage is not UNSET:
            field_dict["leverage"] = leverage
        if interest_rate is not UNSET:
            field_dict["interest_rate"] = interest_rate
        if liquidation_price is not UNSET:
            field_dict["liquidation_price"] = liquidation_price
        if funding_fees is not UNSET:
            field_dict["funding_fees"] = funding_fees
        if trading_mode is not UNSET:
            field_dict["trading_mode"] = trading_mode
        if stoploss_current_dist is not UNSET:
            field_dict["stoploss_current_dist"] = stoploss_current_dist
        if stoploss_current_dist_pct is not UNSET:
            field_dict["stoploss_current_dist_pct"] = stoploss_current_dist_pct
        if stoploss_current_dist_ratio is not UNSET:
            field_dict["stoploss_current_dist_ratio"] = stoploss_current_dist_ratio
        if stoploss_entry_dist is not UNSET:
            field_dict["stoploss_entry_dist"] = stoploss_entry_dist
        if stoploss_entry_dist_ratio is not UNSET:
            field_dict["stoploss_entry_dist_ratio"] = stoploss_entry_dist_ratio
        if open_order is not UNSET:
            field_dict["open_order"] = open_order

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        trade_id = d.pop("trade_id")

        pair = d.pop("pair")

        base_currency = d.pop("base_currency")

        quote_currency = d.pop("quote_currency")

        is_open = d.pop("is_open")

        is_short = d.pop("is_short")

        exchange = d.pop("exchange")

        amount = d.pop("amount")

        amount_requested = d.pop("amount_requested")

        stake_amount = d.pop("stake_amount")

        strategy = d.pop("strategy")

        timeframe = d.pop("timeframe")

        open_date = d.pop("open_date")

        open_timestamp = d.pop("open_timestamp")

        open_rate = d.pop("open_rate")

        open_trade_value = d.pop("open_trade_value")

        orders = []
        _orders = d.pop("orders")
        for orders_item_data in _orders:
            orders_item = OrderSchema.from_dict(orders_item_data)

            orders.append(orders_item)

        current_profit = d.pop("current_profit")

        current_profit_abs = d.pop("current_profit_abs")

        current_profit_pct = d.pop("current_profit_pct")

        current_rate = d.pop("current_rate")

        buy_tag = d.pop("buy_tag", UNSET)

        enter_tag = d.pop("enter_tag", UNSET)

        fee_open = d.pop("fee_open", UNSET)

        fee_open_cost = d.pop("fee_open_cost", UNSET)

        fee_open_currency = d.pop("fee_open_currency", UNSET)

        fee_close = d.pop("fee_close", UNSET)

        fee_close_cost = d.pop("fee_close_cost", UNSET)

        fee_close_currency = d.pop("fee_close_currency", UNSET)

        open_rate_requested = d.pop("open_rate_requested", UNSET)

        close_date = d.pop("close_date", UNSET)

        close_timestamp = d.pop("close_timestamp", UNSET)

        close_rate = d.pop("close_rate", UNSET)

        close_rate_requested = d.pop("close_rate_requested", UNSET)

        close_profit = d.pop("close_profit", UNSET)

        close_profit_pct = d.pop("close_profit_pct", UNSET)

        close_profit_abs = d.pop("close_profit_abs", UNSET)

        profit_ratio = d.pop("profit_ratio", UNSET)

        profit_pct = d.pop("profit_pct", UNSET)

        profit_abs = d.pop("profit_abs", UNSET)

        profit_fiat = d.pop("profit_fiat", UNSET)

        sell_reason = d.pop("sell_reason", UNSET)

        exit_reason = d.pop("exit_reason", UNSET)

        exit_order_status = d.pop("exit_order_status", UNSET)

        stop_loss_abs = d.pop("stop_loss_abs", UNSET)

        stop_loss_ratio = d.pop("stop_loss_ratio", UNSET)

        stop_loss_pct = d.pop("stop_loss_pct", UNSET)

        stoploss_order_id = d.pop("stoploss_order_id", UNSET)

        stoploss_last_update = d.pop("stoploss_last_update", UNSET)

        stoploss_last_update_timestamp = d.pop("stoploss_last_update_timestamp", UNSET)

        initial_stop_loss_abs = d.pop("initial_stop_loss_abs", UNSET)

        initial_stop_loss_ratio = d.pop("initial_stop_loss_ratio", UNSET)

        initial_stop_loss_pct = d.pop("initial_stop_loss_pct", UNSET)

        min_rate = d.pop("min_rate", UNSET)

        max_rate = d.pop("max_rate", UNSET)

        open_order_id = d.pop("open_order_id", UNSET)

        leverage = d.pop("leverage", UNSET)

        interest_rate = d.pop("interest_rate", UNSET)

        liquidation_price = d.pop("liquidation_price", UNSET)

        funding_fees = d.pop("funding_fees", UNSET)

        _trading_mode = d.pop("trading_mode", UNSET)
        trading_mode: Union[Unset, TradingMode]
        if isinstance(_trading_mode, Unset):
            trading_mode = UNSET
        else:
            trading_mode = TradingMode(_trading_mode)

        stoploss_current_dist = d.pop("stoploss_current_dist", UNSET)

        stoploss_current_dist_pct = d.pop("stoploss_current_dist_pct", UNSET)

        stoploss_current_dist_ratio = d.pop("stoploss_current_dist_ratio", UNSET)

        stoploss_entry_dist = d.pop("stoploss_entry_dist", UNSET)

        stoploss_entry_dist_ratio = d.pop("stoploss_entry_dist_ratio", UNSET)

        open_order = d.pop("open_order", UNSET)

        open_trade_schema = cls(
            trade_id=trade_id,
            pair=pair,
            base_currency=base_currency,
            quote_currency=quote_currency,
            is_open=is_open,
            is_short=is_short,
            exchange=exchange,
            amount=amount,
            amount_requested=amount_requested,
            stake_amount=stake_amount,
            strategy=strategy,
            timeframe=timeframe,
            open_date=open_date,
            open_timestamp=open_timestamp,
            open_rate=open_rate,
            open_trade_value=open_trade_value,
            orders=orders,
            current_profit=current_profit,
            current_profit_abs=current_profit_abs,
            current_profit_pct=current_profit_pct,
            current_rate=current_rate,
            buy_tag=buy_tag,
            enter_tag=enter_tag,
            fee_open=fee_open,
            fee_open_cost=fee_open_cost,
            fee_open_currency=fee_open_currency,
            fee_close=fee_close,
            fee_close_cost=fee_close_cost,
            fee_close_currency=fee_close_currency,
            open_rate_requested=open_rate_requested,
            close_date=close_date,
            close_timestamp=close_timestamp,
            close_rate=close_rate,
            close_rate_requested=close_rate_requested,
            close_profit=close_profit,
            close_profit_pct=close_profit_pct,
            close_profit_abs=close_profit_abs,
            profit_ratio=profit_ratio,
            profit_pct=profit_pct,
            profit_abs=profit_abs,
            profit_fiat=profit_fiat,
            sell_reason=sell_reason,
            exit_reason=exit_reason,
            exit_order_status=exit_order_status,
            stop_loss_abs=stop_loss_abs,
            stop_loss_ratio=stop_loss_ratio,
            stop_loss_pct=stop_loss_pct,
            stoploss_order_id=stoploss_order_id,
            stoploss_last_update=stoploss_last_update,
            stoploss_last_update_timestamp=stoploss_last_update_timestamp,
            initial_stop_loss_abs=initial_stop_loss_abs,
            initial_stop_loss_ratio=initial_stop_loss_ratio,
            initial_stop_loss_pct=initial_stop_loss_pct,
            min_rate=min_rate,
            max_rate=max_rate,
            open_order_id=open_order_id,
            leverage=leverage,
            interest_rate=interest_rate,
            liquidation_price=liquidation_price,
            funding_fees=funding_fees,
            trading_mode=trading_mode,
            stoploss_current_dist=stoploss_current_dist,
            stoploss_current_dist_pct=stoploss_current_dist_pct,
            stoploss_current_dist_ratio=stoploss_current_dist_ratio,
            stoploss_entry_dist=stoploss_entry_dist,
            stoploss_entry_dist_ratio=stoploss_entry_dist_ratio,
            open_order=open_order,
        )

        open_trade_schema.additional_properties = d
        return open_trade_schema

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
