from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateImagesAliasesByNameRequest")


@attr.s(auto_attribs=True)
class UpdateImagesAliasesByNameRequest:
    """
    Example:
        {'description': 'New description', 'target': '54c8caac1f61901ed86c68f24af5f5d3672bdc62c71d04f06df3a59e95684473'}

    Attributes:
        description (Union[Unset, str]):  Example: New description.
        target (Union[Unset, str]):  Example: 54c8caac1f61901ed86c68f24af5f5d3672bdc62c71d04f06df3a59e95684473.
    """

    description: Union[Unset, str] = UNSET
    target: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        description = self.description
        target = self.target

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if target is not UNSET:
            field_dict["target"] = target

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        target = d.pop("target", UNSET)

        update_images_aliases_by_name_request = cls(
            description=description,
            target=target,
        )

        update_images_aliases_by_name_request.additional_properties = d
        return update_images_aliases_by_name_request

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
