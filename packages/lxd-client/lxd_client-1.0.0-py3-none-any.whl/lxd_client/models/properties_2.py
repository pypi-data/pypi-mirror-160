from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Properties2")


@attr.s(auto_attribs=True)
class Properties2:
    """
    Example:
        {'os': 'BusyBox', 'name': 'busybox-x86_64', 'description': 'BusyBox x86_64', 'architecture': 'x86_64'}

    Attributes:
        architecture (Union[Unset, str]):  Example: x86_64.
        description (Union[Unset, str]):  Example: BusyBox x86_64.
        name (Union[Unset, str]):  Example: busybox-x86_64.
        os (Union[Unset, str]):  Example: BusyBox.
    """

    architecture: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    os: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        architecture = self.architecture
        description = self.description
        name = self.name
        os = self.os

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if architecture is not UNSET:
            field_dict["architecture"] = architecture
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name
        if os is not UNSET:
            field_dict["os"] = os

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        architecture = d.pop("architecture", UNSET)

        description = d.pop("description", UNSET)

        name = d.pop("name", UNSET)

        os = d.pop("os", UNSET)

        properties_2 = cls(
            architecture=architecture,
            description=description,
            name=name,
            os=os,
        )

        properties_2.additional_properties = d
        return properties_2

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
