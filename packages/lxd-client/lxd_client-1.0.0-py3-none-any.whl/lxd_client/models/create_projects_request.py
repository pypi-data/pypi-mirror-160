from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.features_config import FeaturesConfig
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateProjectsRequest")


@attr.s(auto_attribs=True)
class CreateProjectsRequest:
    """
    Example:
        {'name': 'test', 'description': 'Some description string', 'config': {'features.images': 'true',
            'features.profiles': 'true'}}

    Attributes:
        name (Union[Unset, str]):  Example: test.
        config (Union[Unset, FeaturesConfig]):  Example: {'features.images': 'true', 'features.profiles': 'true'}.
        description (Union[Unset, str]):  Example: Some description string.
    """

    name: Union[Unset, str] = UNSET
    config: Union[Unset, FeaturesConfig] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if config is not UNSET:
            field_dict["config"] = config
        if description is not UNSET:
            field_dict["description"] = description

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

        create_projects_request = cls(
            name=name,
            config=config,
            description=description,
        )

        create_projects_request.additional_properties = d
        return create_projects_request

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
