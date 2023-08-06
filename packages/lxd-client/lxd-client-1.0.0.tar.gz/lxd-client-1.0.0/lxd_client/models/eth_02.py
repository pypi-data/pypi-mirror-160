from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.addresses import Addresses
from ..models.counters import Counters
from ..types import UNSET, Unset

T = TypeVar("T", bound="Eth02")


@attr.s(auto_attribs=True)
class Eth02:
    """
    Attributes:
        addresses (Union[Unset, List[Addresses]]):
        counters (Union[Unset, Counters]):  Example: {'packets_sent': 178, 'packets_received': 402, 'bytes_received':
            33942, 'bytes_sent': 30810}.
        hwaddr (Union[Unset, str]):  Example: 00:16:3e:ec:65:a8.
        host_name (Union[Unset, str]):  Example: vethBWTSU5.
        mtu (Union[Unset, float]):  Example: 1500.
        state (Union[Unset, str]):  Example: up.
        type (Union[Unset, str]):  Example: broadcast.
    """

    addresses: Union[Unset, List[Addresses]] = UNSET
    counters: Union[Unset, Counters] = UNSET
    hwaddr: Union[Unset, str] = UNSET
    host_name: Union[Unset, str] = UNSET
    mtu: Union[Unset, float] = UNSET
    state: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        addresses: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.addresses, Unset):
            addresses = []
            for addresses_item_data in self.addresses:
                addresses_item = addresses_item_data.to_dict()

                addresses.append(addresses_item)

        counters: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.counters, Unset):
            counters = self.counters.to_dict()

        hwaddr = self.hwaddr
        host_name = self.host_name
        mtu = self.mtu
        state = self.state
        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if addresses is not UNSET:
            field_dict["addresses"] = addresses
        if counters is not UNSET:
            field_dict["counters"] = counters
        if hwaddr is not UNSET:
            field_dict["hwaddr"] = hwaddr
        if host_name is not UNSET:
            field_dict["host_name"] = host_name
        if mtu is not UNSET:
            field_dict["mtu"] = mtu
        if state is not UNSET:
            field_dict["state"] = state
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        addresses = []
        _addresses = d.pop("addresses", UNSET)
        for addresses_item_data in _addresses or []:
            addresses_item = Addresses.from_dict(addresses_item_data)

            addresses.append(addresses_item)

        _counters = d.pop("counters", UNSET)
        counters: Union[Unset, Counters]
        if isinstance(_counters, Unset):
            counters = UNSET
        else:
            counters = Counters.from_dict(_counters)

        hwaddr = d.pop("hwaddr", UNSET)

        host_name = d.pop("host_name", UNSET)

        mtu = d.pop("mtu", UNSET)

        state = d.pop("state", UNSET)

        type = d.pop("type", UNSET)

        eth_02 = cls(
            addresses=addresses,
            counters=counters,
            hwaddr=hwaddr,
            host_name=host_name,
            mtu=mtu,
            state=state,
            type=type,
        )

        eth_02.additional_properties = d
        return eth_02

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
