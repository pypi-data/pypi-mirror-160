from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Counters")


@attr.s(auto_attribs=True)
class Counters:
    """
    Example:
        {'packets_sent': 178, 'packets_received': 402, 'bytes_received': 33942, 'bytes_sent': 30810}

    Attributes:
        bytes_received (Union[Unset, float]):  Example: 33942.
        bytes_sent (Union[Unset, float]):  Example: 30810.
        packets_received (Union[Unset, float]):  Example: 402.
        packets_sent (Union[Unset, float]):  Example: 178.
    """

    bytes_received: Union[Unset, float] = UNSET
    bytes_sent: Union[Unset, float] = UNSET
    packets_received: Union[Unset, float] = UNSET
    packets_sent: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        bytes_received = self.bytes_received
        bytes_sent = self.bytes_sent
        packets_received = self.packets_received
        packets_sent = self.packets_sent

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bytes_received is not UNSET:
            field_dict["bytes_received"] = bytes_received
        if bytes_sent is not UNSET:
            field_dict["bytes_sent"] = bytes_sent
        if packets_received is not UNSET:
            field_dict["packets_received"] = packets_received
        if packets_sent is not UNSET:
            field_dict["packets_sent"] = packets_sent

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        bytes_received = d.pop("bytes_received", UNSET)

        bytes_sent = d.pop("bytes_sent", UNSET)

        packets_received = d.pop("packets_received", UNSET)

        packets_sent = d.pop("packets_sent", UNSET)

        counters = cls(
            bytes_received=bytes_received,
            bytes_sent=bytes_sent,
            packets_received=packets_received,
            packets_sent=packets_sent,
        )

        counters.additional_properties = d
        return counters

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
