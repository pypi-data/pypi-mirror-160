from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateNetworksByNameRequest")


@attr.s(auto_attribs=True)
class UpdateNetworksByNameRequest:
    """
    Example:
        {'bridge.driver': 'openvswitch', 'ipv4.address': '10.0.3.1/24', 'ipv6.address': 'fd1:6997:4939:495d::1/64'}

    Attributes:
        bridge_driver (Union[Unset, str]):  Example: openvswitch.
        ipv4_address (Union[Unset, str]):  Example: 10.0.3.1/24.
        ipv6_address (Union[Unset, str]):  Example: fd1:6997:4939:495d::1/64.
    """

    bridge_driver: Union[Unset, str] = UNSET
    ipv4_address: Union[Unset, str] = UNSET
    ipv6_address: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        bridge_driver = self.bridge_driver
        ipv4_address = self.ipv4_address
        ipv6_address = self.ipv6_address

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bridge_driver is not UNSET:
            field_dict["bridge.driver"] = bridge_driver
        if ipv4_address is not UNSET:
            field_dict["ipv4.address"] = ipv4_address
        if ipv6_address is not UNSET:
            field_dict["ipv6.address"] = ipv6_address

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        bridge_driver = d.pop("bridge.driver", UNSET)

        ipv4_address = d.pop("ipv4.address", UNSET)

        ipv6_address = d.pop("ipv6.address", UNSET)

        update_networks_by_name_request = cls(
            bridge_driver=bridge_driver,
            ipv4_address=ipv4_address,
            ipv6_address=ipv6_address,
        )

        update_networks_by_name_request.additional_properties = d
        return update_networks_by_name_request

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
