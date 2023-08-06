from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Addresses")


@attr.s(auto_attribs=True)
class Addresses:
    """
    Example:
        {'address': '10.0.3.27', 'netmask': '24', 'scope': '24', 'family': 'init'}

    Attributes:
        family (Union[Unset, str]):  Example: init.
        address (Union[Unset, str]):  Example: 10.0.3.27.
        netmask (Union[Unset, str]):  Example: 24.
        scope (Union[Unset, str]):  Example: 24.
    """

    family: Union[Unset, str] = UNSET
    address: Union[Unset, str] = UNSET
    netmask: Union[Unset, str] = UNSET
    scope: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        family = self.family
        address = self.address
        netmask = self.netmask
        scope = self.scope

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if family is not UNSET:
            field_dict["family"] = family
        if address is not UNSET:
            field_dict["address"] = address
        if netmask is not UNSET:
            field_dict["netmask"] = netmask
        if scope is not UNSET:
            field_dict["scope"] = scope

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        family = d.pop("family", UNSET)

        address = d.pop("address", UNSET)

        netmask = d.pop("netmask", UNSET)

        scope = d.pop("scope", UNSET)

        addresses = cls(
            family=family,
            address=address,
            netmask=netmask,
            scope=scope,
        )

        addresses.additional_properties = d
        return addresses

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
