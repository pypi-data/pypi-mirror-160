from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.order_type_values import OrderTypeValues
from ..types import UNSET, Unset

T = TypeVar("T", bound="OrderTypes")


@attr.s(auto_attribs=True)
class OrderTypes:
    """
    Attributes:
        entry (OrderTypeValues): An enumeration.
        exit_ (OrderTypeValues): An enumeration.
        stoploss (OrderTypeValues): An enumeration.
        stoploss_on_exchange (bool):
        emergency_exit (Union[Unset, OrderTypeValues]): An enumeration.
        force_exit (Union[Unset, OrderTypeValues]): An enumeration.
        force_entry (Union[Unset, OrderTypeValues]): An enumeration.
        stoploss_on_exchange_interval (Union[Unset, int]):
    """

    entry: OrderTypeValues
    exit_: OrderTypeValues
    stoploss: OrderTypeValues
    stoploss_on_exchange: bool
    emergency_exit: Union[Unset, OrderTypeValues] = UNSET
    force_exit: Union[Unset, OrderTypeValues] = UNSET
    force_entry: Union[Unset, OrderTypeValues] = UNSET
    stoploss_on_exchange_interval: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        entry = self.entry.value

        exit_ = self.exit_.value

        stoploss = self.stoploss.value

        stoploss_on_exchange = self.stoploss_on_exchange
        emergency_exit: Union[Unset, str] = UNSET
        if not isinstance(self.emergency_exit, Unset):
            emergency_exit = self.emergency_exit.value

        force_exit: Union[Unset, str] = UNSET
        if not isinstance(self.force_exit, Unset):
            force_exit = self.force_exit.value

        force_entry: Union[Unset, str] = UNSET
        if not isinstance(self.force_entry, Unset):
            force_entry = self.force_entry.value

        stoploss_on_exchange_interval = self.stoploss_on_exchange_interval

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entry": entry,
                "exit": exit_,
                "stoploss": stoploss,
                "stoploss_on_exchange": stoploss_on_exchange,
            }
        )
        if emergency_exit is not UNSET:
            field_dict["emergency_exit"] = emergency_exit
        if force_exit is not UNSET:
            field_dict["force_exit"] = force_exit
        if force_entry is not UNSET:
            field_dict["force_entry"] = force_entry
        if stoploss_on_exchange_interval is not UNSET:
            field_dict["stoploss_on_exchange_interval"] = stoploss_on_exchange_interval

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entry = OrderTypeValues(d.pop("entry"))

        exit_ = OrderTypeValues(d.pop("exit"))

        stoploss = OrderTypeValues(d.pop("stoploss"))

        stoploss_on_exchange = d.pop("stoploss_on_exchange")

        _emergency_exit = d.pop("emergency_exit", UNSET)
        emergency_exit: Union[Unset, OrderTypeValues]
        if isinstance(_emergency_exit, Unset):
            emergency_exit = UNSET
        else:
            emergency_exit = OrderTypeValues(_emergency_exit)

        _force_exit = d.pop("force_exit", UNSET)
        force_exit: Union[Unset, OrderTypeValues]
        if isinstance(_force_exit, Unset):
            force_exit = UNSET
        else:
            force_exit = OrderTypeValues(_force_exit)

        _force_entry = d.pop("force_entry", UNSET)
        force_entry: Union[Unset, OrderTypeValues]
        if isinstance(_force_entry, Unset):
            force_entry = UNSET
        else:
            force_entry = OrderTypeValues(_force_entry)

        stoploss_on_exchange_interval = d.pop("stoploss_on_exchange_interval", UNSET)

        order_types = cls(
            entry=entry,
            exit_=exit_,
            stoploss=stoploss,
            stoploss_on_exchange=stoploss_on_exchange,
            emergency_exit=emergency_exit,
            force_exit=force_exit,
            force_entry=force_entry,
            stoploss_on_exchange_interval=stoploss_on_exchange_interval,
        )

        order_types.additional_properties = d
        return order_types

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
