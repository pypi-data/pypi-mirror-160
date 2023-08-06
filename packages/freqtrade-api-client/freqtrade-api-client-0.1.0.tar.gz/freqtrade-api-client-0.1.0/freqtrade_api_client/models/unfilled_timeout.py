from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UnfilledTimeout")


@attr.s(auto_attribs=True)
class UnfilledTimeout:
    """
    Attributes:
        entry (Union[Unset, int]):
        exit_ (Union[Unset, int]):
        unit (Union[Unset, str]):
        exit_timeout_count (Union[Unset, int]):
    """

    entry: Union[Unset, int] = UNSET
    exit_: Union[Unset, int] = UNSET
    unit: Union[Unset, str] = UNSET
    exit_timeout_count: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        entry = self.entry
        exit_ = self.exit_
        unit = self.unit
        exit_timeout_count = self.exit_timeout_count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if entry is not UNSET:
            field_dict["entry"] = entry
        if exit_ is not UNSET:
            field_dict["exit"] = exit_
        if unit is not UNSET:
            field_dict["unit"] = unit
        if exit_timeout_count is not UNSET:
            field_dict["exit_timeout_count"] = exit_timeout_count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entry = d.pop("entry", UNSET)

        exit_ = d.pop("exit", UNSET)

        unit = d.pop("unit", UNSET)

        exit_timeout_count = d.pop("exit_timeout_count", UNSET)

        unfilled_timeout = cls(
            entry=entry,
            exit_=exit_,
            unit=unit,
            exit_timeout_count=exit_timeout_count,
        )

        unfilled_timeout.additional_properties = d
        return unfilled_timeout

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
