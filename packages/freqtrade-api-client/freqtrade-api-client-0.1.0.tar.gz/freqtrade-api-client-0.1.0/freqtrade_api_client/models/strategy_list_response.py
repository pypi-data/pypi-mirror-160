from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="StrategyListResponse")


@attr.s(auto_attribs=True)
class StrategyListResponse:
    """
    Attributes:
        strategies (List[str]):
    """

    strategies: List[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        strategies = self.strategies

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "strategies": strategies,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        strategies = cast(List[str], d.pop("strategies"))

        strategy_list_response = cls(
            strategies=strategies,
        )

        strategy_list_response.additional_properties = d
        return strategy_list_response

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
