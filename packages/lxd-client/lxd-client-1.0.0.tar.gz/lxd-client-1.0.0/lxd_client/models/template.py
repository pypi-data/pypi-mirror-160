from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.template_properties import TemplateProperties
from ..types import UNSET, Unset

T = TypeVar("T", bound="Template")


@attr.s(auto_attribs=True)
class Template:
    """
    Example:
        {'template': 'template.tpl', 'when': ['when', 'when'], 'create_only': False, 'properties': '{}'}

    Attributes:
        when (Union[Unset, List[str]]):
        create_only (Union[Unset, bool]):
        template (Union[Unset, str]):  Example: template.tpl.
        properties (Union[Unset, TemplateProperties]):
    """

    when: Union[Unset, List[str]] = UNSET
    create_only: Union[Unset, bool] = UNSET
    template: Union[Unset, str] = UNSET
    properties: Union[Unset, TemplateProperties] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        when: Union[Unset, List[str]] = UNSET
        if not isinstance(self.when, Unset):
            when = self.when

        create_only = self.create_only
        template = self.template
        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if when is not UNSET:
            field_dict["when"] = when
        if create_only is not UNSET:
            field_dict["create_only"] = create_only
        if template is not UNSET:
            field_dict["template"] = template
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        when = cast(List[str], d.pop("when", UNSET))

        create_only = d.pop("create_only", UNSET)

        template = d.pop("template", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, TemplateProperties]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = TemplateProperties.from_dict(_properties)

        template = cls(
            when=when,
            create_only=create_only,
            template=template,
            properties=properties,
        )

        template.additional_properties = d
        return template

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
