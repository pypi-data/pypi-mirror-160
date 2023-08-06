from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="DeleteTrade")


@attr.s(auto_attribs=True)
class DeleteTrade:
    """
    Attributes:
        cancel_order_count (int):
        result (str):
        result_msg (str):
        trade_id (int):
    """

    cancel_order_count: int
    result: str
    result_msg: str
    trade_id: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cancel_order_count = self.cancel_order_count
        result = self.result
        result_msg = self.result_msg
        trade_id = self.trade_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cancel_order_count": cancel_order_count,
                "result": result,
                "result_msg": result_msg,
                "trade_id": trade_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        cancel_order_count = d.pop("cancel_order_count")

        result = d.pop("result")

        result_msg = d.pop("result_msg")

        trade_id = d.pop("trade_id")

        delete_trade = cls(
            cancel_order_count=cancel_order_count,
            result=result,
            result_msg=result_msg,
            trade_id=trade_id,
        )

        delete_trade.additional_properties = d
        return delete_trade

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
