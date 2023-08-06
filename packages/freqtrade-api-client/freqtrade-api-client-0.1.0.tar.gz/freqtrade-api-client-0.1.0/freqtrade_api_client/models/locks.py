from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.lock_model import LockModel

T = TypeVar("T", bound="Locks")


@attr.s(auto_attribs=True)
class Locks:
    """
    Attributes:
        lock_count (int):
        locks (List[LockModel]):
    """

    lock_count: int
    locks: List[LockModel]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        lock_count = self.lock_count
        locks = []
        for locks_item_data in self.locks:
            locks_item = locks_item_data.to_dict()

            locks.append(locks_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "lock_count": lock_count,
                "locks": locks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        lock_count = d.pop("lock_count")

        locks = []
        _locks = d.pop("locks")
        for locks_item_data in _locks:
            locks_item = LockModel.from_dict(locks_item_data)

            locks.append(locks_item)

        locks = cls(
            lock_count=lock_count,
            locks=locks,
        )

        locks.additional_properties = d
        return locks

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
