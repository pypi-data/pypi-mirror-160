from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.devices_kvm import DevicesKvm
from ..models.memory_limits_config import MemoryLimitsConfig
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateProfilesByNameRequest")


@attr.s(auto_attribs=True)
class UpdateProfilesByNameRequest:
    """
    Example:
        {'devices': {'kvm': {'path': '/dev/kvm', 'type': 'unix-char'}}, 'description': 'Some description string',
            'config': {'limits.memory': '2GB'}}

    Attributes:
        config (Union[Unset, MemoryLimitsConfig]):  Example: {'limits.memory': '2GB'}.
        description (Union[Unset, str]):  Example: Some description string.
        devices (Union[Unset, DevicesKvm]):  Example: {'kvm': {'path': '/dev/kvm', 'type': 'unix-char'}}.
    """

    config: Union[Unset, MemoryLimitsConfig] = UNSET
    description: Union[Unset, str] = UNSET
    devices: Union[Unset, DevicesKvm] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        description = self.description
        devices: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.devices, Unset):
            devices = self.devices.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config is not UNSET:
            field_dict["config"] = config
        if description is not UNSET:
            field_dict["description"] = description
        if devices is not UNSET:
            field_dict["devices"] = devices

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _config = d.pop("config", UNSET)
        config: Union[Unset, MemoryLimitsConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = MemoryLimitsConfig.from_dict(_config)

        description = d.pop("description", UNSET)

        _devices = d.pop("devices", UNSET)
        devices: Union[Unset, DevicesKvm]
        if isinstance(_devices, Unset):
            devices = UNSET
        else:
            devices = DevicesKvm.from_dict(_devices)

        update_profiles_by_name_request = cls(
            config=config,
            description=description,
            devices=devices,
        )

        update_profiles_by_name_request.additional_properties = d
        return update_profiles_by_name_request

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
