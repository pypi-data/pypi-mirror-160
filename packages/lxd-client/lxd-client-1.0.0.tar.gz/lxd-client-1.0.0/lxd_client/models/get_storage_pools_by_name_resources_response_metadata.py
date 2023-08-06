from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.space_inodes import SpaceInodes
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetStoragePoolsByNameResourcesResponseMetadata")


@attr.s(auto_attribs=True)
class GetStoragePoolsByNameResourcesResponseMetadata:
    """
    Attributes:
        space (Union[Unset, SpaceInodes]):
        inodes (Union[Unset, SpaceInodes]):
    """

    space: Union[Unset, SpaceInodes] = UNSET
    inodes: Union[Unset, SpaceInodes] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        space: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.space, Unset):
            space = self.space.to_dict()

        inodes: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.inodes, Unset):
            inodes = self.inodes.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if space is not UNSET:
            field_dict["space"] = space
        if inodes is not UNSET:
            field_dict["inodes"] = inodes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _space = d.pop("space", UNSET)
        space: Union[Unset, SpaceInodes]
        if isinstance(_space, Unset):
            space = UNSET
        else:
            space = SpaceInodes.from_dict(_space)

        _inodes = d.pop("inodes", UNSET)
        inodes: Union[Unset, SpaceInodes]
        if isinstance(_inodes, Unset):
            inodes = UNSET
        else:
            inodes = SpaceInodes.from_dict(_inodes)

        get_storage_pools_by_name_resources_response_metadata = cls(
            space=space,
            inodes=inodes,
        )

        get_storage_pools_by_name_resources_response_metadata.additional_properties = d
        return get_storage_pools_by_name_resources_response_metadata

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
