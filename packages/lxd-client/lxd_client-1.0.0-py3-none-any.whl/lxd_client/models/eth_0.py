from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Eth0")


@attr.s(auto_attribs=True)
class Eth0:
    """
    Example:
        {'nictype': 'bridged', 'parent': 'lxdbr0', 'name': 'eth0', 'type': 'nic'}

    Attributes:
        name (Union[Unset, str]):  Example: eth0.
        nictype (Union[Unset, str]):  Example: bridged.
        parent (Union[Unset, str]):  Example: lxdbr0.
        type (Union[Unset, str]):  Example: nic.
    """

    name: Union[Unset, str] = UNSET
    nictype: Union[Unset, str] = UNSET
    parent: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        nictype = self.nictype
        parent = self.parent
        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if nictype is not UNSET:
            field_dict["nictype"] = nictype
        if parent is not UNSET:
            field_dict["parent"] = parent
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        nictype = d.pop("nictype", UNSET)

        parent = d.pop("parent", UNSET)

        type = d.pop("type", UNSET)

        eth_0 = cls(
            name=name,
            nictype=nictype,
            parent=parent,
            type=type,
        )

        eth_0.additional_properties = d
        return eth_0

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
