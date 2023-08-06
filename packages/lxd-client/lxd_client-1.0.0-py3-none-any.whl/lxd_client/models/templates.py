from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.template import Template
from ..types import UNSET, Unset

T = TypeVar("T", bound="Templates")


@attr.s(auto_attribs=True)
class Templates:
    """
    Example:
        {'/template': {'template': 'template.tpl', 'when': ['when', 'when'], 'create_only': False, 'properties': '{}'}}

    Attributes:
        template (Union[Unset, Template]):  Example: {'template': 'template.tpl', 'when': ['when', 'when'],
            'create_only': False, 'properties': '{}'}.
    """

    template: Union[Unset, Template] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        template: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.template, Unset):
            template = self.template.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if template is not UNSET:
            field_dict["/template"] = template

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _template = d.pop("/template", UNSET)
        template: Union[Unset, Template]
        if isinstance(_template, Unset):
            template = UNSET
        else:
            template = Template.from_dict(_template)

        templates = cls(
            template=template,
        )

        templates.additional_properties = d
        return templates

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
