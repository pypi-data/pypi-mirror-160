from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateImagesAliasesRequest")


@attr.s(auto_attribs=True)
class CreateImagesAliasesRequest:
    """
    Example:
        {'name': 'alias-name', 'description': 'The alias description', 'target': 'SHA-256'}

    Attributes:
        description (Union[Unset, str]):  Example: The alias description.
        target (Union[Unset, str]):  Example: SHA-256.
        name (Union[Unset, str]):  Example: alias-name.
    """

    description: Union[Unset, str] = UNSET
    target: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        description = self.description
        target = self.target
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if target is not UNSET:
            field_dict["target"] = target
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        target = d.pop("target", UNSET)

        name = d.pop("name", UNSET)

        create_images_aliases_request = cls(
            description=description,
            target=target,
            name=name,
        )

        create_images_aliases_request.additional_properties = d
        return create_images_aliases_request

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
