from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.features_config import FeaturesConfig
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetProjectsByNameResponse")


@attr.s(auto_attribs=True)
class GetProjectsByNameResponse:
    """
    Example:
        {'name': 'test', 'description': 'Some description string', 'config': {'features.images': 'true',
            'features.profiles': 'true'}, 'used_by': ['/1.0/instances/blah']}

    Attributes:
        name (Union[Unset, str]):  Example: test.
        config (Union[Unset, FeaturesConfig]):  Example: {'features.images': 'true', 'features.profiles': 'true'}.
        description (Union[Unset, str]):  Example: Some description string.
        used_by (Union[Unset, List[str]]):  Example: ['/1.0/instances/blah'].
    """

    name: Union[Unset, str] = UNSET
    config: Union[Unset, FeaturesConfig] = UNSET
    description: Union[Unset, str] = UNSET
    used_by: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        description = self.description
        used_by: Union[Unset, List[str]] = UNSET
        if not isinstance(self.used_by, Unset):
            used_by = self.used_by

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if config is not UNSET:
            field_dict["config"] = config
        if description is not UNSET:
            field_dict["description"] = description
        if used_by is not UNSET:
            field_dict["used_by"] = used_by

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        _config = d.pop("config", UNSET)
        config: Union[Unset, FeaturesConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = FeaturesConfig.from_dict(_config)

        description = d.pop("description", UNSET)

        used_by = cast(List[str], d.pop("used_by", UNSET))

        get_projects_by_name_response = cls(
            name=name,
            config=config,
            description=description,
            used_by=used_by,
        )

        get_projects_by_name_response.additional_properties = d
        return get_projects_by_name_response

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
