from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="Logs")


@attr.s(auto_attribs=True)
class Logs:
    """
    Attributes:
        log_count (int):
        logs (List[List[Any]]):
    """

    log_count: int
    logs: List[List[Any]]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        log_count = self.log_count
        logs = []
        for logs_item_data in self.logs:
            logs_item = logs_item_data

            logs.append(logs_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "log_count": log_count,
                "logs": logs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        log_count = d.pop("log_count")

        logs = []
        _logs = d.pop("logs")
        for logs_item_data in _logs:
            logs_item = cast(List[Any], logs_item_data)

            logs.append(logs_item)

        logs = cls(
            log_count=log_count,
            logs=logs,
        )

        logs.additional_properties = d
        return logs

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
