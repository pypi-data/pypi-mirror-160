from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetImagesAliasesByNameResponse")


@attr.s(auto_attribs=True)
class GetImagesAliasesByNameResponse:
    """
    Example:
        {'name': 'test', 'description': 'my description', 'target':
            'c9b6e738fae75286d52f497415463a8ecc61bbcb046536f220d797b0e500a41f'}

    Attributes:
        name (Union[Unset, str]):  Example: test.
        description (Union[Unset, str]):  Example: my description.
        target (Union[Unset, str]):  Example: c9b6e738fae75286d52f497415463a8ecc61bbcb046536f220d797b0e500a41f.
        type (Union[Unset, str]):  Example: container.
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    target: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        target = self.target
        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if target is not UNSET:
            field_dict["target"] = target
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        target = d.pop("target", UNSET)

        type = d.pop("type", UNSET)

        get_images_aliases_by_name_response = cls(
            name=name,
            description=description,
            target=target,
            type=type,
        )

        get_images_aliases_by_name_response.additional_properties = d
        return get_images_aliases_by_name_response

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
