from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.volume_block_file_system_config import VolumeBlockFileSystemConfig
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchStoragePoolsByNameRequest")


@attr.s(auto_attribs=True)
class PatchStoragePoolsByNameRequest:
    """
    Example:
        {'config': {'volume.block.filesystem': 'xfs'}}

    Attributes:
        config (Union[Unset, VolumeBlockFileSystemConfig]):  Example: {'volume.block.filesystem': 'xfs'}.
    """

    config: Union[Unset, VolumeBlockFileSystemConfig] = UNSET
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
        config: Union[Unset, VolumeBlockFileSystemConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = VolumeBlockFileSystemConfig.from_dict(_config)

        patch_storage_pools_by_name_request = cls(
            config=config,
        )

        patch_storage_pools_by_name_request.additional_properties = d
        return patch_storage_pools_by_name_request

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
