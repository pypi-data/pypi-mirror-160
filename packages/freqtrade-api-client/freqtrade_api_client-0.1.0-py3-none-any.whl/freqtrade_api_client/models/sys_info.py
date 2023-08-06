from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="SysInfo")


@attr.s(auto_attribs=True)
class SysInfo:
    """
    Attributes:
        cpu_pct (List[float]):
        ram_pct (float):
    """

    cpu_pct: List[float]
    ram_pct: float
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cpu_pct = self.cpu_pct

        ram_pct = self.ram_pct

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cpu_pct": cpu_pct,
                "ram_pct": ram_pct,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        cpu_pct = cast(List[float], d.pop("cpu_pct"))

        ram_pct = d.pop("ram_pct")

        sys_info = cls(
            cpu_pct=cpu_pct,
            ram_pct=ram_pct,
        )

        sys_info.additional_properties = d
        return sys_info

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
