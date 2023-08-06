from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Properties")


@attr.s(auto_attribs=True)
class Properties:
    """
    Example:
        {'os': 'ubuntu', 'release': '18.04', 'architecture': 'x86_64'}

    Attributes:
        os (Union[Unset, str]):  Example: ubuntu.
        release (Union[Unset, str]):  Example: 18.04.
        architecture (Union[Unset, str]):  Example: x86_64.
    """

    os: Union[Unset, str] = UNSET
    release: Union[Unset, str] = UNSET
    architecture: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        os = self.os
        release = self.release
        architecture = self.architecture

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if os is not UNSET:
            field_dict["os"] = os
        if release is not UNSET:
            field_dict["release"] = release
        if architecture is not UNSET:
            field_dict["architecture"] = architecture

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        os = d.pop("os", UNSET)

        release = d.pop("release", UNSET)

        architecture = d.pop("architecture", UNSET)

        properties = cls(
            os=os,
            release=release,
            architecture=architecture,
        )

        properties.additional_properties = d
        return properties

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
