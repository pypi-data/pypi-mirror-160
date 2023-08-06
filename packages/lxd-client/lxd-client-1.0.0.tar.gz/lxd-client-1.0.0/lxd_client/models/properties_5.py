from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Properties5")


@attr.s(auto_attribs=True)
class Properties5:
    """
    Example:
        {'os': 'ubuntu', 'release': 'bionic'}

    Attributes:
        os (Union[Unset, str]):  Example: ubuntu.
        release (Union[Unset, str]):  Example: bionic.
    """

    os: Union[Unset, str] = UNSET
    release: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        os = self.os
        release = self.release

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if os is not UNSET:
            field_dict["os"] = os
        if release is not UNSET:
            field_dict["release"] = release

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        os = d.pop("os", UNSET)

        release = d.pop("release", UNSET)

        properties_5 = cls(
            os=os,
            release=release,
        )

        properties_5.additional_properties = d
        return properties_5

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
