from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.devices_kvm import DevicesKvm
from ..models.memory_limits_config import MemoryLimitsConfig
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetProfilesByNameResponse")


@attr.s(auto_attribs=True)
class GetProfilesByNameResponse:
    """
    Example:
        {'devices': {'kvm': {'path': '/dev/kvm', 'type': 'unix-char'}}, 'name': 'test', 'description': 'Some description
            string', 'config': {'limits.memory': '2GB'}, 'used_by': ['/1.0/instances/blah']}

    Attributes:
        name (Union[Unset, str]):  Example: test.
        description (Union[Unset, str]):  Example: Some description string.
        config (Union[Unset, MemoryLimitsConfig]):  Example: {'limits.memory': '2GB'}.
        devices (Union[Unset, DevicesKvm]):  Example: {'kvm': {'path': '/dev/kvm', 'type': 'unix-char'}}.
        used_by (Union[Unset, List[str]]):  Example: ['/1.0/instances/blah'].
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    config: Union[Unset, MemoryLimitsConfig] = UNSET
    devices: Union[Unset, DevicesKvm] = UNSET
    used_by: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        devices: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.devices, Unset):
            devices = self.devices.to_dict()

        used_by: Union[Unset, List[str]] = UNSET
        if not isinstance(self.used_by, Unset):
            used_by = self.used_by

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if config is not UNSET:
            field_dict["config"] = config
        if devices is not UNSET:
            field_dict["devices"] = devices
        if used_by is not UNSET:
            field_dict["used_by"] = used_by

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        _config = d.pop("config", UNSET)
        config: Union[Unset, MemoryLimitsConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = MemoryLimitsConfig.from_dict(_config)

        _devices = d.pop("devices", UNSET)
        devices: Union[Unset, DevicesKvm]
        if isinstance(_devices, Unset):
            devices = UNSET
        else:
            devices = DevicesKvm.from_dict(_devices)

        used_by = cast(List[str], d.pop("used_by", UNSET))

        get_profiles_by_name_response = cls(
            name=name,
            description=description,
            config=config,
            devices=devices,
            used_by=used_by,
        )

        get_profiles_by_name_response.additional_properties = d
        return get_profiles_by_name_response

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
