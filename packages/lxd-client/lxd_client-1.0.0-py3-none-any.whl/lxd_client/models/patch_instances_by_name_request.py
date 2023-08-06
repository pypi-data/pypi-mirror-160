from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.cpu_config import CpuConfig
from ..models.devices_3 import Devices3
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchInstancesByNameRequest")


@attr.s(auto_attribs=True)
class PatchInstancesByNameRequest:
    """
    Example:
        {'devices': {'root': {'path': '/', 'size': '5GB', 'pool': 'default'}}, 'ephemeral': True, 'config':
            {'limits.cpu': '3'}}

    Attributes:
        config (Union[Unset, CpuConfig]):  Example: {'limits.cpu': '3'}.
        devices (Union[Unset, Devices3]):  Example: {'root': {'path': '/', 'size': '5GB', 'pool': 'default'}}.
        ephemeral (Union[Unset, bool]):  Example: True.
    """

    config: Union[Unset, CpuConfig] = UNSET
    devices: Union[Unset, Devices3] = UNSET
    ephemeral: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        devices: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.devices, Unset):
            devices = self.devices.to_dict()

        ephemeral = self.ephemeral

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config is not UNSET:
            field_dict["config"] = config
        if devices is not UNSET:
            field_dict["devices"] = devices
        if ephemeral is not UNSET:
            field_dict["ephemeral"] = ephemeral

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _config = d.pop("config", UNSET)
        config: Union[Unset, CpuConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = CpuConfig.from_dict(_config)

        _devices = d.pop("devices", UNSET)
        devices: Union[Unset, Devices3]
        if isinstance(_devices, Unset):
            devices = UNSET
        else:
            devices = Devices3.from_dict(_devices)

        ephemeral = d.pop("ephemeral", UNSET)

        patch_instances_by_name_request = cls(
            config=config,
            devices=devices,
            ephemeral=ephemeral,
        )

        patch_instances_by_name_request.additional_properties = d
        return patch_instances_by_name_request

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
