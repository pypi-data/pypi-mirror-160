from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FileSystemMountOptionsAndThinPoolConfig")


@attr.s(auto_attribs=True)
class FileSystemMountOptionsAndThinPoolConfig:
    """
    Example:
        {'lvm.vg_name': 'pool1', 'volume.block.filesystem': 'xfs', 'volume.block.mount_options': 'discard', 'size':
            '15032385536', 'lvm.thinpool_name': 'LXDThinPool', 'source': 'pool1', 'volume.size': '10737418240', 'used_by':
            'used_by'}

    Attributes:
        size (Union[Unset, str]):  Example: 15032385536.
        source (Union[Unset, str]):  Example: pool1.
        used_by (Union[Unset, str]):
        volume_block_filesystem (Union[Unset, str]):  Example: xfs.
        volume_block_mount_options (Union[Unset, str]):  Example: discard.
        lvm_thinpool_name (Union[Unset, str]):  Example: LXDThinPool.
        lvm_vg_name (Union[Unset, str]):  Example: pool1.
        volume_size (Union[Unset, str]):  Example: 10737418240.
    """

    size: Union[Unset, str] = UNSET
    source: Union[Unset, str] = UNSET
    used_by: Union[Unset, str] = UNSET
    volume_block_filesystem: Union[Unset, str] = UNSET
    volume_block_mount_options: Union[Unset, str] = UNSET
    lvm_thinpool_name: Union[Unset, str] = UNSET
    lvm_vg_name: Union[Unset, str] = UNSET
    volume_size: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        size = self.size
        source = self.source
        used_by = self.used_by
        volume_block_filesystem = self.volume_block_filesystem
        volume_block_mount_options = self.volume_block_mount_options
        lvm_thinpool_name = self.lvm_thinpool_name
        lvm_vg_name = self.lvm_vg_name
        volume_size = self.volume_size

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if size is not UNSET:
            field_dict["size"] = size
        if source is not UNSET:
            field_dict["source"] = source
        if used_by is not UNSET:
            field_dict["used_by"] = used_by
        if volume_block_filesystem is not UNSET:
            field_dict["volume.block.filesystem"] = volume_block_filesystem
        if volume_block_mount_options is not UNSET:
            field_dict["volume.block.mount_options"] = volume_block_mount_options
        if lvm_thinpool_name is not UNSET:
            field_dict["lvm.thinpool_name"] = lvm_thinpool_name
        if lvm_vg_name is not UNSET:
            field_dict["lvm.vg_name"] = lvm_vg_name
        if volume_size is not UNSET:
            field_dict["volume.size"] = volume_size

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        size = d.pop("size", UNSET)

        source = d.pop("source", UNSET)

        used_by = d.pop("used_by", UNSET)

        volume_block_filesystem = d.pop("volume.block.filesystem", UNSET)

        volume_block_mount_options = d.pop("volume.block.mount_options", UNSET)

        lvm_thinpool_name = d.pop("lvm.thinpool_name", UNSET)

        lvm_vg_name = d.pop("lvm.vg_name", UNSET)

        volume_size = d.pop("volume.size", UNSET)

        file_system_mount_options_and_thin_pool_config = cls(
            size=size,
            source=source,
            used_by=used_by,
            volume_block_filesystem=volume_block_filesystem,
            volume_block_mount_options=volume_block_mount_options,
            lvm_thinpool_name=lvm_thinpool_name,
            lvm_vg_name=lvm_vg_name,
            volume_size=volume_size,
        )

        file_system_mount_options_and_thin_pool_config.additional_properties = d
        return file_system_mount_options_and_thin_pool_config

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
