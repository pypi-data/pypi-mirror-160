from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="OrderSchema")


@attr.s(auto_attribs=True)
class OrderSchema:
    """
    Attributes:
        pair (str):
        order_id (str):
        status (str):
        remaining (float):
        amount (float):
        safe_price (float):
        cost (float):
        filled (float):
        ft_order_side (str):
        order_type (str):
        is_open (bool):
        order_timestamp (Union[Unset, int]):
        order_filled_timestamp (Union[Unset, int]):
    """

    pair: str
    order_id: str
    status: str
    remaining: float
    amount: float
    safe_price: float
    cost: float
    filled: float
    ft_order_side: str
    order_type: str
    is_open: bool
    order_timestamp: Union[Unset, int] = UNSET
    order_filled_timestamp: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pair = self.pair
        order_id = self.order_id
        status = self.status
        remaining = self.remaining
        amount = self.amount
        safe_price = self.safe_price
        cost = self.cost
        filled = self.filled
        ft_order_side = self.ft_order_side
        order_type = self.order_type
        is_open = self.is_open
        order_timestamp = self.order_timestamp
        order_filled_timestamp = self.order_filled_timestamp

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pair": pair,
                "order_id": order_id,
                "status": status,
                "remaining": remaining,
                "amount": amount,
                "safe_price": safe_price,
                "cost": cost,
                "filled": filled,
                "ft_order_side": ft_order_side,
                "order_type": order_type,
                "is_open": is_open,
            }
        )
        if order_timestamp is not UNSET:
            field_dict["order_timestamp"] = order_timestamp
        if order_filled_timestamp is not UNSET:
            field_dict["order_filled_timestamp"] = order_filled_timestamp

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pair = d.pop("pair")

        order_id = d.pop("order_id")

        status = d.pop("status")

        remaining = d.pop("remaining")

        amount = d.pop("amount")

        safe_price = d.pop("safe_price")

        cost = d.pop("cost")

        filled = d.pop("filled")

        ft_order_side = d.pop("ft_order_side")

        order_type = d.pop("order_type")

        is_open = d.pop("is_open")

        order_timestamp = d.pop("order_timestamp", UNSET)

        order_filled_timestamp = d.pop("order_filled_timestamp", UNSET)

        order_schema = cls(
            pair=pair,
            order_id=order_id,
            status=status,
            remaining=remaining,
            amount=amount,
            safe_price=safe_price,
            cost=cost,
            filled=filled,
            ft_order_side=ft_order_side,
            order_type=order_type,
            is_open=is_open,
            order_timestamp=order_timestamp,
            order_filled_timestamp=order_filled_timestamp,
        )

        order_schema.additional_properties = d
        return order_schema

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
