from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.disk_and_lvm_config import DiskAndLvmConfig
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateStoragePoolsByNameRequest")


@attr.s(auto_attribs=True)
class UpdateStoragePoolsByNameRequest:
    """
    Example:
        {'config': {'lvm.vg_name': 'pool1', 'volume.block.filesystem': 'xfs', 'volume.block.mount_options': 'discard',
            'size': '15032385536', 'lvm.thinpool_name': 'LXDThinPool', 'source': 'pool1', 'volume.size': '10737418240'}}

    Attributes:
        config (Union[Unset, DiskAndLvmConfig]):  Example: {'lvm.vg_name': 'pool1', 'volume.block.filesystem': 'xfs',
            'volume.block.mount_options': 'discard', 'size': '15032385536', 'lvm.thinpool_name': 'LXDThinPool', 'source':
            'pool1', 'volume.size': '10737418240'}.
    """

    config: Union[Unset, DiskAndLvmConfig] = UNSET
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
        config: Union[Unset, DiskAndLvmConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = DiskAndLvmConfig.from_dict(_config)

        update_storage_pools_by_name_request = cls(
            config=config,
        )

        update_storage_pools_by_name_request.additional_properties = d
        return update_storage_pools_by_name_request

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
