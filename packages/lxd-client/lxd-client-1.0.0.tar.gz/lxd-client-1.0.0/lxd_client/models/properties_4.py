from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Properties4")


@attr.s(auto_attribs=True)
class Properties4:
    """
    Example:
        {'os': 'ubuntu', 'release': 'bionic', 'description': 'Ubuntu 18.04 LTS server (20180601)', 'architecture':
            'x86_64'}

    Attributes:
        architecture (Union[Unset, str]):  Example: x86_64.
        description (Union[Unset, str]):  Example: Ubuntu 18.04 LTS server (20180601).
        release (Union[Unset, str]):  Example: bionic.
        os (Union[Unset, str]):  Example: ubuntu.
    """

    architecture: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    release: Union[Unset, str] = UNSET
    os: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        architecture = self.architecture
        description = self.description
        release = self.release
        os = self.os

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if architecture is not UNSET:
            field_dict["architecture"] = architecture
        if description is not UNSET:
            field_dict["description"] = description
        if release is not UNSET:
            field_dict["release"] = release
        if os is not UNSET:
            field_dict["os"] = os

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        architecture = d.pop("architecture", UNSET)

        description = d.pop("description", UNSET)

        release = d.pop("release", UNSET)

        os = d.pop("os", UNSET)

        properties_4 = cls(
            architecture=architecture,
            description=description,
            release=release,
            os=os,
        )

        properties_4.additional_properties = d
        return properties_4

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
