from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.file_system_mount_options_and_thin_pool_config import FileSystemMountOptionsAndThinPoolConfig
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateStoragePoolsByNameVolumesByTypeNameRequest2")


@attr.s(auto_attribs=True)
class UpdateStoragePoolsByNameVolumesByTypeNameRequest2:
    """
    Example:
        {'config': {'lvm.vg_name': 'pool1', 'volume.block.filesystem': 'xfs', 'volume.block.mount_options': 'discard',
            'size': '15032385536', 'lvm.thinpool_name': 'LXDThinPool', 'source': 'pool1', 'volume.size': '10737418240',
            'used_by': 'used_by'}}

    Attributes:
        config (Union[Unset, FileSystemMountOptionsAndThinPoolConfig]):  Example: {'lvm.vg_name': 'pool1',
            'volume.block.filesystem': 'xfs', 'volume.block.mount_options': 'discard', 'size': '15032385536',
            'lvm.thinpool_name': 'LXDThinPool', 'source': 'pool1', 'volume.size': '10737418240', 'used_by': 'used_by'}.
    """

    config: Union[Unset, FileSystemMountOptionsAndThinPoolConfig] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config is not UNSET:
            field_dict["config"] = config

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _config = d.pop("config", UNSET)
        config: Union[Unset, FileSystemMountOptionsAndThinPoolConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = FileSystemMountOptionsAndThinPoolConfig.from_dict(_config)

        update_storage_pools_by_name_volumes_by_type_name_request_2 = cls(
            config=config,
        )

        update_storage_pools_by_name_volumes_by_type_name_request_2.additional_properties = d
        return update_storage_pools_by_name_volumes_by_type_name_request_2

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
