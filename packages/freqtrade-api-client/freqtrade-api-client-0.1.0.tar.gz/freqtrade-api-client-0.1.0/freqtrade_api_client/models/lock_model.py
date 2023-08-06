from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="LockModel")


@attr.s(auto_attribs=True)
class LockModel:
    """
    Attributes:
        id (int):
        active (bool):
        lock_end_time (str):
        lock_end_timestamp (int):
        lock_time (str):
        lock_timestamp (int):
        pair (str):
        side (str):
        reason (str):
    """

    id: int
    active: bool
    lock_end_time: str
    lock_end_timestamp: int
    lock_time: str
    lock_timestamp: int
    pair: str
    side: str
    reason: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        active = self.active
        lock_end_time = self.lock_end_time
        lock_end_timestamp = self.lock_end_timestamp
        lock_time = self.lock_time
        lock_timestamp = self.lock_timestamp
        pair = self.pair
        side = self.side
        reason = self.reason

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "active": active,
                "lock_end_time": lock_end_time,
                "lock_end_timestamp": lock_end_timestamp,
                "lock_time": lock_time,
                "lock_timestamp": lock_timestamp,
                "pair": pair,
                "side": side,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        active = d.pop("active")

        lock_end_time = d.pop("lock_end_time")

        lock_end_timestamp = d.pop("lock_end_timestamp")

        lock_time = d.pop("lock_time")

        lock_timestamp = d.pop("lock_timestamp")

        pair = d.pop("pair")

        side = d.pop("side")

        reason = d.pop("reason")

        lock_model = cls(
            id=id,
            active=active,
            lock_end_time=lock_end_time,
            lock_end_timestamp=lock_end_timestamp,
            lock_time=lock_time,
            lock_timestamp=lock_timestamp,
            pair=pair,
            side=side,
            reason=reason,
        )

        lock_model.additional_properties = d
        return lock_model

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
