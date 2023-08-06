from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="SellReason")


@attr.s(auto_attribs=True)
class SellReason:
    """
    Attributes:
        wins (int):
        losses (int):
        draws (int):
    """

    wins: int
    losses: int
    draws: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        wins = self.wins
        losses = self.losses
        draws = self.draws

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "wins": wins,
                "losses": losses,
                "draws": draws,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        wins = d.pop("wins")

        losses = d.pop("losses")

        draws = d.pop("draws")

        sell_reason = cls(
            wins=wins,
            losses=losses,
            draws=draws,
        )

        sell_reason.additional_properties = d
        return sell_reason

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
