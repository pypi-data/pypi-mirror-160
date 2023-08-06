from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.order_type_values import OrderTypeValues
from ..models.signal_direction import SignalDirection
from ..types import UNSET, Unset

T = TypeVar("T", bound="ForceEnterPayload")


@attr.s(auto_attribs=True)
class ForceEnterPayload:
    """
    Attributes:
        pair (str):
        side (Union[Unset, SignalDirection]): An enumeration. Default: SignalDirection.LONG.
        price (Union[Unset, float]):
        ordertype (Union[Unset, OrderTypeValues]): An enumeration.
        stakeamount (Union[Unset, float]):
        entry_tag (Union[Unset, str]):
    """

    pair: str
    side: Union[Unset, SignalDirection] = SignalDirection.LONG
    price: Union[Unset, float] = UNSET
    ordertype: Union[Unset, OrderTypeValues] = UNSET
    stakeamount: Union[Unset, float] = UNSET
    entry_tag: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pair = self.pair
        side: Union[Unset, str] = UNSET
        if not isinstance(self.side, Unset):
            side = self.side.value

        price = self.price
        ordertype: Union[Unset, str] = UNSET
        if not isinstance(self.ordertype, Unset):
            ordertype = self.ordertype.value

        stakeamount = self.stakeamount
        entry_tag = self.entry_tag

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pair": pair,
            }
        )
        if side is not UNSET:
            field_dict["side"] = side
        if price is not UNSET:
            field_dict["price"] = price
        if ordertype is not UNSET:
            field_dict["ordertype"] = ordertype
        if stakeamount is not UNSET:
            field_dict["stakeamount"] = stakeamount
        if entry_tag is not UNSET:
            field_dict["entry_tag"] = entry_tag

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pair = d.pop("pair")

        _side = d.pop("side", UNSET)
        side: Union[Unset, SignalDirection]
        if isinstance(_side, Unset):
            side = UNSET
        else:
            side = SignalDirection(_side)

        price = d.pop("price", UNSET)

        _ordertype = d.pop("ordertype", UNSET)
        ordertype: Union[Unset, OrderTypeValues]
        if isinstance(_ordertype, Unset):
            ordertype = UNSET
        else:
            ordertype = OrderTypeValues(_ordertype)

        stakeamount = d.pop("stakeamount", UNSET)

        entry_tag = d.pop("entry_tag", UNSET)

        force_enter_payload = cls(
            pair=pair,
            side=side,
            price=price,
            ordertype=ordertype,
            stakeamount=stakeamount,
            entry_tag=entry_tag,
        )

        force_enter_payload.additional_properties = d
        return force_enter_payload

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
