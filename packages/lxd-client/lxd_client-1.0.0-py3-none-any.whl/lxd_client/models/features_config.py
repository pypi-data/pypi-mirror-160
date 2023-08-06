from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FeaturesConfig")


@attr.s(auto_attribs=True)
class FeaturesConfig:
    """
    Example:
        {'features.images': 'true', 'features.profiles': 'true'}

    Attributes:
        features_images (Union[Unset, str]):  Example: true.
        features_profiles (Union[Unset, str]):  Example: true.
    """

    features_images: Union[Unset, str] = UNSET
    features_profiles: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        features_images = self.features_images
        features_profiles = self.features_profiles

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if features_images is not UNSET:
            field_dict["features.images"] = features_images
        if features_profiles is not UNSET:
            field_dict["features.profiles"] = features_profiles

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        features_images = d.pop("features.images", UNSET)

        features_profiles = d.pop("features.profiles", UNSET)

        features_config = cls(
            features_images=features_images,
            features_profiles=features_profiles,
        )

        features_config.additional_properties = d
        return features_config

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
