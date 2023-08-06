from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.balance import Balance

T = TypeVar("T", bound="Balances")


@attr.s(auto_attribs=True)
class Balances:
    """
    Attributes:
        currencies (List[Balance]):
        total (float):
        symbol (str):
        value (float):
        stake (str):
        note (str):
        starting_capital (float):
        starting_capital_ratio (float):
        starting_capital_pct (float):
        starting_capital_fiat (float):
        starting_capital_fiat_ratio (float):
        starting_capital_fiat_pct (float):
    """

    currencies: List[Balance]
    total: float
    symbol: str
    value: float
    stake: str
    note: str
    starting_capital: float
    starting_capital_ratio: float
    starting_capital_pct: float
    starting_capital_fiat: float
    starting_capital_fiat_ratio: float
    starting_capital_fiat_pct: float
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        currencies = []
        for currencies_item_data in self.currencies:
            currencies_item = currencies_item_data.to_dict()

            currencies.append(currencies_item)

        total = self.total
        symbol = self.symbol
        value = self.value
        stake = self.stake
        note = self.note
        starting_capital = self.starting_capital
        starting_capital_ratio = self.starting_capital_ratio
        starting_capital_pct = self.starting_capital_pct
        starting_capital_fiat = self.starting_capital_fiat
        starting_capital_fiat_ratio = self.starting_capital_fiat_ratio
        starting_capital_fiat_pct = self.starting_capital_fiat_pct

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "currencies": currencies,
                "total": total,
                "symbol": symbol,
                "value": value,
                "stake": stake,
                "note": note,
                "starting_capital": starting_capital,
                "starting_capital_ratio": starting_capital_ratio,
                "starting_capital_pct": starting_capital_pct,
                "starting_capital_fiat": starting_capital_fiat,
                "starting_capital_fiat_ratio": starting_capital_fiat_ratio,
                "starting_capital_fiat_pct": starting_capital_fiat_pct,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        currencies = []
        _currencies = d.pop("currencies")
        for currencies_item_data in _currencies:
            currencies_item = Balance.from_dict(currencies_item_data)

            currencies.append(currencies_item)

        total = d.pop("total")

        symbol = d.pop("symbol")

        value = d.pop("value")

        stake = d.pop("stake")

        note = d.pop("note")

        starting_capital = d.pop("starting_capital")

        starting_capital_ratio = d.pop("starting_capital_ratio")

        starting_capital_pct = d.pop("starting_capital_pct")

        starting_capital_fiat = d.pop("starting_capital_fiat")

        starting_capital_fiat_ratio = d.pop("starting_capital_fiat_ratio")

        starting_capital_fiat_pct = d.pop("starting_capital_fiat_pct")

        balances = cls(
            currencies=currencies,
            total=total,
            symbol=symbol,
            value=value,
            stake=stake,
            note=note,
            starting_capital=starting_capital,
            starting_capital_ratio=starting_capital_ratio,
            starting_capital_pct=starting_capital_pct,
            starting_capital_fiat=starting_capital_fiat,
            starting_capital_fiat_ratio=starting_capital_fiat_ratio,
            starting_capital_fiat_pct=starting_capital_fiat_pct,
        )

        balances.additional_properties = d
        return balances

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
