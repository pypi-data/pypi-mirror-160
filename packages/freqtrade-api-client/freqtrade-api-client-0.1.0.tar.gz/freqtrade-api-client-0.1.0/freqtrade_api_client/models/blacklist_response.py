from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.blacklist_response_errors import BlacklistResponseErrors

T = TypeVar("T", bound="BlacklistResponse")


@attr.s(auto_attribs=True)
class BlacklistResponse:
    """
    Attributes:
        blacklist (List[str]):
        blacklist_expanded (List[str]):
        errors (BlacklistResponseErrors):
        length (int):
        method (List[str]):
    """

    blacklist: List[str]
    blacklist_expanded: List[str]
    errors: BlacklistResponseErrors
    length: int
    method: List[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        blacklist = self.blacklist

        blacklist_expanded = self.blacklist_expanded

        errors = self.errors.to_dict()

        length = self.length
        method = self.method

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "blacklist": blacklist,
                "blacklist_expanded": blacklist_expanded,
                "errors": errors,
                "length": length,
                "method": method,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        blacklist = cast(List[str], d.pop("blacklist"))

        blacklist_expanded = cast(List[str], d.pop("blacklist_expanded"))

        errors = BlacklistResponseErrors.from_dict(d.pop("errors"))

        length = d.pop("length")

        method = cast(List[str], d.pop("method"))

        blacklist_response = cls(
            blacklist=blacklist,
            blacklist_expanded=blacklist_expanded,
            errors=errors,
            length=length,
            method=method,
        )

        blacklist_response.additional_properties = d
        return blacklist_response

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
