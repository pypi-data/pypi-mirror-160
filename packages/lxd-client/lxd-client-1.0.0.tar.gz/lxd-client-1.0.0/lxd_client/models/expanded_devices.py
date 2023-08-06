from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.eth_0 import Eth0
from ..models.root import Root
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExpandedDevices")


@attr.s(auto_attribs=True)
class ExpandedDevices:
    """
    Example:
        {'root': {'path': '/', 'type': 'disk'}, 'eth0': {'nictype': 'bridged', 'parent': 'lxdbr0', 'name': 'eth0',
            'type': 'nic'}}

    Attributes:
        eth0 (Union[Unset, Eth0]):  Example: {'nictype': 'bridged', 'parent': 'lxdbr0', 'name': 'eth0', 'type': 'nic'}.
        root (Union[Unset, Root]):  Example: {'path': '/', 'type': 'disk'}.
    """

    eth0: Union[Unset, Eth0] = UNSET
    root: Union[Unset, Root] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        eth0: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.eth0, Unset):
            eth0 = self.eth0.to_dict()

        root: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.root, Unset):
            root = self.root.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if eth0 is not UNSET:
            field_dict["eth0"] = eth0
        if root is not UNSET:
            field_dict["root"] = root

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _eth0 = d.pop("eth0", UNSET)
        eth0: Union[Unset, Eth0]
        if isinstance(_eth0, Unset):
            eth0 = UNSET
        else:
            eth0 = Eth0.from_dict(_eth0)

        _root = d.pop("root", UNSET)
        root: Union[Unset, Root]
        if isinstance(_root, Unset):
            root = UNSET
        else:
            root = Root.from_dict(_root)

        expanded_devices = cls(
            eth0=eth0,
            root=root,
        )

        expanded_devices.additional_properties = d
        return expanded_devices

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
