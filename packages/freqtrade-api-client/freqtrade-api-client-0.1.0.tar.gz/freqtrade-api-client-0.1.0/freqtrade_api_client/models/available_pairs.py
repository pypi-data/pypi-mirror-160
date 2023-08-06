from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="AvailablePairs")


@attr.s(auto_attribs=True)
class AvailablePairs:
    """
    Attributes:
        length (int):
        pairs (List[str]):
        pair_interval (List[List[str]]):
    """

    length: int
    pairs: List[str]
    pair_interval: List[List[str]]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        length = self.length
        pairs = self.pairs

        pair_interval = []
        for pair_interval_item_data in self.pair_interval:
            pair_interval_item = pair_interval_item_data

            pair_interval.append(pair_interval_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "length": length,
                "pairs": pairs,
                "pair_interval": pair_interval,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        length = d.pop("length")

        pairs = cast(List[str], d.pop("pairs"))

        pair_interval = []
        _pair_interval = d.pop("pair_interval")
        for pair_interval_item_data in _pair_interval:
            pair_interval_item = cast(List[str], pair_interval_item_data)

            pair_interval.append(pair_interval_item)

        available_pairs = cls(
            length=length,
            pairs=pairs,
            pair_interval=pair_interval,
        )

        available_pairs.additional_properties = d
        return available_pairs

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
