from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NetworkIPConfig")


@attr.s(auto_attribs=True)
class NetworkIPConfig:
    """
    Example:
        {'ipv4.address': 'none', 'ipv6.nat': 'true', 'ipv6.address': '2001:470:b368:4242::1/64'}

    Attributes:
        ipv4_address (Union[Unset, str]):  Example: none.
        ipv6_address (Union[Unset, str]):  Example: 2001:470:b368:4242::1/64.
        ipv6_nat (Union[Unset, str]):  Example: true.
    """

    ipv4_address: Union[Unset, str] = UNSET
    ipv6_address: Union[Unset, str] = UNSET
    ipv6_nat: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        ipv4_address = self.ipv4_address
        ipv6_address = self.ipv6_address
        ipv6_nat = self.ipv6_nat

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if ipv4_address is not UNSET:
            field_dict["ipv4.address"] = ipv4_address
        if ipv6_address is not UNSET:
            field_dict["ipv6.address"] = ipv6_address
        if ipv6_nat is not UNSET:
            field_dict["ipv6.nat"] = ipv6_nat

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        ipv4_address = d.pop("ipv4.address", UNSET)

        ipv6_address = d.pop("ipv6.address", UNSET)

        ipv6_nat = d.pop("ipv6.nat", UNSET)

        network_ip_config = cls(
            ipv4_address=ipv4_address,
            ipv6_address=ipv6_address,
            ipv6_nat=ipv6_nat,
        )

        network_ip_config.additional_properties = d
        return network_ip_config

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
