from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.daily_record import DailyRecord

T = TypeVar("T", bound="Daily")


@attr.s(auto_attribs=True)
class Daily:
    """
    Attributes:
        data (List[DailyRecord]):
        fiat_display_currency (str):
        stake_currency (str):
    """

    data: List[DailyRecord]
    fiat_display_currency: str
    stake_currency: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()

            data.append(data_item)

        fiat_display_currency = self.fiat_display_currency
        stake_currency = self.stake_currency

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "fiat_display_currency": fiat_display_currency,
                "stake_currency": stake_currency,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = DailyRecord.from_dict(data_item_data)

            data.append(data_item)

        fiat_display_currency = d.pop("fiat_display_currency")

        stake_currency = d.pop("stake_currency")

        daily = cls(
            data=data,
            fiat_display_currency=fiat_display_currency,
            stake_currency=stake_currency,
        )

        daily.additional_properties = d
        return daily

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
