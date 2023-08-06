from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.root_2 import Root2
from ..types import UNSET, Unset

T = TypeVar("T", bound="Devices3")


@attr.s(auto_attribs=True)
class Devices3:
    """
    Example:
        {'root': {'path': '/', 'size': '5GB', 'pool': 'default'}}

    Attributes:
        root (Union[Unset, Root2]):  Example: {'path': '/', 'size': '5GB', 'pool': 'default'}.
    """

    root: Union[Unset, Root2] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        root: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.root, Unset):
            root = self.root.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if root is not UNSET:
            field_dict["root"] = root

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _root = d.pop("root", UNSET)
        root: Union[Unset, Root2]
        if isinstance(_root, Unset):
            root = UNSET
        else:
            root = Root2.from_dict(_root)

        devices_3 = cls(
            root=root,
        )

        devices_3.additional_properties = d
        return devices_3

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
