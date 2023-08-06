from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="Balance")


@attr.s(auto_attribs=True)
class Balance:
    """
    Attributes:
        currency (str):
        free (float):
        balance (float):
        used (float):
        est_stake (float):
        stake (str):
        side (str):
        leverage (float):
        is_position (bool):
        position (float):
    """

    currency: str
    free: float
    balance: float
    used: float
    est_stake: float
    stake: str
    side: str
    leverage: float
    is_position: bool
    position: float
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        currency = self.currency
        free = self.free
        balance = self.balance
        used = self.used
        est_stake = self.est_stake
        stake = self.stake
        side = self.side
        leverage = self.leverage
        is_position = self.is_position
        position = self.position

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "currency": currency,
                "free": free,
                "balance": balance,
                "used": used,
                "est_stake": est_stake,
                "stake": stake,
                "side": side,
                "leverage": leverage,
                "is_position": is_position,
                "position": position,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        currency = d.pop("currency")

        free = d.pop("free")

        balance = d.pop("balance")

        used = d.pop("used")

        est_stake = d.pop("est_stake")

        stake = d.pop("stake")

        side = d.pop("side")

        leverage = d.pop("leverage")

        is_position = d.pop("is_position")

        position = d.pop("position")

        balance = cls(
            currency=currency,
            free=free,
            balance=balance,
            used=used,
            est_stake=est_stake,
            stake=stake,
            side=side,
            leverage=leverage,
            is_position=is_position,
            position=position,
        )

        balance.additional_properties = d
        return balance

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
