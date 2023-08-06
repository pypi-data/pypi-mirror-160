from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DiskConfig")


@attr.s(auto_attribs=True)
class DiskConfig:
    """
    Attributes:
        size (Union[Unset, str]):  Example: 61203283968.
        source (Union[Unset, str]):  Example: /home/chb/mnt/l2/disks/default.img.
        volume_size (Union[Unset, str]):  Example: 0.
        zfs_pool_name (Union[Unset, str]):  Example: default.
    """

    size: Union[Unset, str] = UNSET
    source: Union[Unset, str] = UNSET
    volume_size: Union[Unset, str] = UNSET
    zfs_pool_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        size = self.size
        source = self.source
        volume_size = self.volume_size
        zfs_pool_name = self.zfs_pool_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if size is not UNSET:
            field_dict["size"] = size
        if source is not UNSET:
            field_dict["source"] = source
        if volume_size is not UNSET:
            field_dict["volume.size"] = volume_size
        if zfs_pool_name is not UNSET:
            field_dict["zfs.pool_name"] = zfs_pool_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        size = d.pop("size", UNSET)

        source = d.pop("source", UNSET)

        volume_size = d.pop("volume.size", UNSET)

        zfs_pool_name = d.pop("zfs.pool_name", UNSET)

        disk_config = cls(
            size=size,
            source=source,
            volume_size=volume_size,
            zfs_pool_name=zfs_pool_name,
        )

        disk_config.additional_properties = d
        return disk_config

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
