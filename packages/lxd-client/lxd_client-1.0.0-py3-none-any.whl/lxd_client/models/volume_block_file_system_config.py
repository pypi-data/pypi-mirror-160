from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="VolumeBlockFileSystemConfig")


@attr.s(auto_attribs=True)
class VolumeBlockFileSystemConfig:
    """
    Example:
        {'volume.block.filesystem': 'xfs'}

    Attributes:
        volume_block_filesystem (Union[Unset, str]):  Example: xfs.
    """

    volume_block_filesystem: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        volume_block_filesystem = self.volume_block_filesystem

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if volume_block_filesystem is not UNSET:
            field_dict["volume.block.filesystem"] = volume_block_filesystem

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        volume_block_filesystem = d.pop("volume.block.filesystem", UNSET)

        volume_block_file_system_config = cls(
            volume_block_filesystem=volume_block_filesystem,
        )

        volume_block_file_system_config.additional_properties = d
        return volume_block_file_system_config

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
