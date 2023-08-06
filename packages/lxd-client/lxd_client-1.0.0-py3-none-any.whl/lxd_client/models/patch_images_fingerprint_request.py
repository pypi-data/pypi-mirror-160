from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.properties_5 import Properties5
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchImagesFingerprintRequest")


@attr.s(auto_attribs=True)
class PatchImagesFingerprintRequest:
    """
    Example:
        {'public': True, 'properties': {'os': 'ubuntu', 'release': 'bionic'}}

    Attributes:
        properties (Union[Unset, Properties5]):  Example: {'os': 'ubuntu', 'release': 'bionic'}.
        public (Union[Unset, bool]):  Example: True.
    """

    properties: Union[Unset, Properties5] = UNSET
    public: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        public = self.public

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if properties is not UNSET:
            field_dict["properties"] = properties
        if public is not UNSET:
            field_dict["public"] = public

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, Properties5]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = Properties5.from_dict(_properties)

        public = d.pop("public", UNSET)

        patch_images_fingerprint_request = cls(
            properties=properties,
            public=public,
        )

        patch_images_fingerprint_request.additional_properties = d
        return patch_images_fingerprint_request

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
