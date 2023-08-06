import datetime
from typing import Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

T = TypeVar("T", bound="Health")


@attr.s(auto_attribs=True)
class Health:
    """
    Attributes:
        last_process (datetime.datetime):
        last_process_ts (int):
    """

    last_process: datetime.datetime
    last_process_ts: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        last_process = self.last_process.isoformat()

        last_process_ts = self.last_process_ts

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "last_process": last_process,
                "last_process_ts": last_process_ts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        last_process = isoparse(d.pop("last_process"))

        last_process_ts = d.pop("last_process_ts")

        health = cls(
            last_process=last_process,
            last_process_ts=last_process_ts,
        )

        health.additional_properties = d
        return health

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
