from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.block_file_system_and_mount_options_config import BlockFileSystemAndMountOptionsConfig
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetStoragePoolsByNameVolumesByTypeNameResponseMetadata")


@attr.s(auto_attribs=True)
class GetStoragePoolsByNameVolumesByTypeNameResponseMetadata:
    """
    Attributes:
        type (Union[Unset, str]):  Example: custom.
        used_by (Union[Unset, List[str]]):
        name (Union[Unset, str]):  Example: vol1.
        config (Union[Unset, BlockFileSystemAndMountOptionsConfig]):
    """

    type: Union[Unset, str] = UNSET
    used_by: Union[Unset, List[str]] = UNSET
    name: Union[Unset, str] = UNSET
    config: Union[Unset, BlockFileSystemAndMountOptionsConfig] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        used_by: Union[Unset, List[str]] = UNSET
        if not isinstance(self.used_by, Unset):
            used_by = self.used_by

        name = self.name
        config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if used_by is not UNSET:
            field_dict["used_by"] = used_by
        if name is not UNSET:
            field_dict["name"] = name
        if config is not UNSET:
            field_dict["config"] = config

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type", UNSET)

        used_by = cast(List[str], d.pop("used_by", UNSET))

        name = d.pop("name", UNSET)

        _config = d.pop("config", UNSET)
        config: Union[Unset, BlockFileSystemAndMountOptionsConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = BlockFileSystemAndMountOptionsConfig.from_dict(_config)

        get_storage_pools_by_name_volumes_by_type_name_response_metadata = cls(
            type=type,
            used_by=used_by,
            name=name,
            config=config,
        )

        get_storage_pools_by_name_volumes_by_type_name_response_metadata.additional_properties = d
        return get_storage_pools_by_name_volumes_by_type_name_response_metadata

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
