from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.properties_2 import Properties2
from ..models.templates import Templates
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetInstancesByNameMetadataResponse")


@attr.s(auto_attribs=True)
class GetInstancesByNameMetadataResponse:
    """
    Example:
        {'expiry_date': 0, 'templates': {'/template': {'template': 'template.tpl', 'when': ['when', 'when'],
            'create_only': False, 'properties': '{}'}}, 'creation_date': 1477146654, 'properties': {'os': 'BusyBox', 'name':
            'busybox-x86_64', 'description': 'BusyBox x86_64', 'architecture': 'x86_64'}, 'architecture': 'x86_64'}

    Attributes:
        architecture (Union[Unset, str]):  Example: x86_64.
        creation_date (Union[Unset, float]):  Example: 1477146654.
        expiry_date (Union[Unset, float]):
        properties (Union[Unset, Properties2]):  Example: {'os': 'BusyBox', 'name': 'busybox-x86_64', 'description':
            'BusyBox x86_64', 'architecture': 'x86_64'}.
        templates (Union[Unset, Templates]):  Example: {'/template': {'template': 'template.tpl', 'when': ['when',
            'when'], 'create_only': False, 'properties': '{}'}}.
    """

    architecture: Union[Unset, str] = UNSET
    creation_date: Union[Unset, float] = UNSET
    expiry_date: Union[Unset, float] = UNSET
    properties: Union[Unset, Properties2] = UNSET
    templates: Union[Unset, Templates] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        architecture = self.architecture
        creation_date = self.creation_date
        expiry_date = self.expiry_date
        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        templates: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.templates, Unset):
            templates = self.templates.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if architecture is not UNSET:
            field_dict["architecture"] = architecture
        if creation_date is not UNSET:
            field_dict["creation_date"] = creation_date
        if expiry_date is not UNSET:
            field_dict["expiry_date"] = expiry_date
        if properties is not UNSET:
            field_dict["properties"] = properties
        if templates is not UNSET:
            field_dict["templates"] = templates

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        architecture = d.pop("architecture", UNSET)

        creation_date = d.pop("creation_date", UNSET)

        expiry_date = d.pop("expiry_date", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, Properties2]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = Properties2.from_dict(_properties)

        _templates = d.pop("templates", UNSET)
        templates: Union[Unset, Templates]
        if isinstance(_templates, Unset):
            templates = UNSET
        else:
            templates = Templates.from_dict(_templates)

        get_instances_by_name_metadata_response = cls(
            architecture=architecture,
            creation_date=creation_date,
            expiry_date=expiry_date,
            properties=properties,
            templates=templates,
        )

        get_instances_by_name_metadata_response.additional_properties = d
        return get_instances_by_name_metadata_response

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
