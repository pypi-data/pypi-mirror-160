from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="BlockFileSystemAndMountOptionsConfig")


@attr.s(auto_attribs=True)
class BlockFileSystemAndMountOptionsConfig:
    """
    Attributes:
        block_filesystem (Union[Unset, str]):  Example: ext4.
        block_mount_options (Union[Unset, str]):  Example: discard.
        size (Union[Unset, str]):  Example: 10737418240.
    """

    block_filesystem: Union[Unset, str] = UNSET
    block_mount_options: Union[Unset, str] = UNSET
    size: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        block_filesystem = self.block_filesystem
        block_mount_options = self.block_mount_options
        size = self.size

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if block_filesystem is not UNSET:
            field_dict["block.filesystem"] = block_filesystem
        if block_mount_options is not UNSET:
            field_dict["block.mount_options"] = block_mount_options
        if size is not UNSET:
            field_dict["size"] = size

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        block_filesystem = d.pop("block.filesystem", UNSET)

        block_mount_options = d.pop("block.mount_options", UNSET)

        size = d.pop("size", UNSET)

        block_file_system_and_mount_options_config = cls(
            block_filesystem=block_filesystem,
            block_mount_options=block_mount_options,
            size=size,
        )

        block_file_system_and_mount_options_config.additional_properties = d
        return block_file_system_and_mount_options_config

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
