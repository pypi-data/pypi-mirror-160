from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.devices_root import DevicesRoot
from ..models.expanded_config import ExpandedConfig
from ..models.expanded_devices import ExpandedDevices
from ..models.hardware_specs_config import HardwareSpecsConfig
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetInstancesByNameResponse")


@attr.s(auto_attribs=True)
class GetInstancesByNameResponse:
    """
    Example:
        {'status_code': 103, 'devices': {'root': {'path': '/', 'type': 'disk'}}, 'profiles': ['profiles', 'profiles'],
            'created_at': '2016-02-16T01:05:05.000Z', 'ephemeral': False, 'expanded_config': {'limits.cpu': '3',
            'volatile.eth0.hwaddr': '00:16:3e:1c:94:38', 'volatile.base_image':
            '97d97a3d1d053840ca19c86cdd0596cf1be060c5157d31407f2a4f9f350c78cc'}, 'expanded_devices': {'root': {'path': '/',
            'type': 'disk'}, 'eth0': {'nictype': 'bridged', 'parent': 'lxdbr0', 'name': 'eth0', 'type': 'nic'}},
            'last_used_at': '2016-02-16T01:05:05.000Z', 'name': 'my-instance', 'config': {'limits.cpu': '3',
            'volatile.eth0.hwaddr': '00:16:3e:1c:94:38', 'volatile.base_image':
            '97d97a3d1d053840ca19c86cdd0596cf1be060c5157d31407f2a4f9f350c78cc'}, 'stateful': False, 'architecture':
            'x86_64', 'status': 'Running'}

    Attributes:
        architecture (Union[Unset, str]):  Example: x86_64.
        config (Union[Unset, HardwareSpecsConfig]):  Example: {'limits.cpu': '3', 'volatile.eth0.hwaddr':
            '00:16:3e:1c:94:38', 'volatile.base_image': '97d97a3d1d053840ca19c86cdd0596cf1be060c5157d31407f2a4f9f350c78cc'}.
        created_at (Union[Unset, str]):  Example: 2016-02-16T01:05:05.000Z.
        devices (Union[Unset, DevicesRoot]):  Example: {'root': {'path': '/', 'type': 'disk'}}.
        ephemeral (Union[Unset, bool]):
        expanded_config (Union[Unset, ExpandedConfig]):  Example: {'limits.cpu': '3', 'volatile.eth0.hwaddr':
            '00:16:3e:1c:94:38', 'volatile.base_image': '97d97a3d1d053840ca19c86cdd0596cf1be060c5157d31407f2a4f9f350c78cc'}.
        expanded_devices (Union[Unset, ExpandedDevices]):  Example: {'root': {'path': '/', 'type': 'disk'}, 'eth0':
            {'nictype': 'bridged', 'parent': 'lxdbr0', 'name': 'eth0', 'type': 'nic'}}.
        last_used_at (Union[Unset, str]):  Example: 2016-02-16T01:05:05.000Z.
        name (Union[Unset, str]):  Example: my-instance.
        profiles (Union[Unset, List[str]]):
        stateful (Union[Unset, bool]): If true, indicates that the instance has some stored state that can be restored
            on startup
        status (Union[Unset, str]):  Example: Running.
        status_code (Union[Unset, int]):  Example: 103.
    """

    architecture: Union[Unset, str] = UNSET
    config: Union[Unset, HardwareSpecsConfig] = UNSET
    created_at: Union[Unset, str] = UNSET
    devices: Union[Unset, DevicesRoot] = UNSET
    ephemeral: Union[Unset, bool] = UNSET
    expanded_config: Union[Unset, ExpandedConfig] = UNSET
    expanded_devices: Union[Unset, ExpandedDevices] = UNSET
    last_used_at: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    profiles: Union[Unset, List[str]] = UNSET
    stateful: Union[Unset, bool] = UNSET
    status: Union[Unset, str] = UNSET
    status_code: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        architecture = self.architecture
        config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        created_at = self.created_at
        devices: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.devices, Unset):
            devices = self.devices.to_dict()

        ephemeral = self.ephemeral
        expanded_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.expanded_config, Unset):
            expanded_config = self.expanded_config.to_dict()

        expanded_devices: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.expanded_devices, Unset):
            expanded_devices = self.expanded_devices.to_dict()

        last_used_at = self.last_used_at
        name = self.name
        profiles: Union[Unset, List[str]] = UNSET
        if not isinstance(self.profiles, Unset):
            profiles = self.profiles

        stateful = self.stateful
        status = self.status
        status_code = self.status_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if architecture is not UNSET:
            field_dict["architecture"] = architecture
        if config is not UNSET:
            field_dict["config"] = config
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if devices is not UNSET:
            field_dict["devices"] = devices
        if ephemeral is not UNSET:
            field_dict["ephemeral"] = ephemeral
        if expanded_config is not UNSET:
            field_dict["expanded_config"] = expanded_config
        if expanded_devices is not UNSET:
            field_dict["expanded_devices"] = expanded_devices
        if last_used_at is not UNSET:
            field_dict["last_used_at"] = last_used_at
        if name is not UNSET:
            field_dict["name"] = name
        if profiles is not UNSET:
            field_dict["profiles"] = profiles
        if stateful is not UNSET:
            field_dict["stateful"] = stateful
        if status is not UNSET:
            field_dict["status"] = status
        if status_code is not UNSET:
            field_dict["status_code"] = status_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        architecture = d.pop("architecture", UNSET)

        _config = d.pop("config", UNSET)
        config: Union[Unset, HardwareSpecsConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = HardwareSpecsConfig.from_dict(_config)

        created_at = d.pop("created_at", UNSET)

        _devices = d.pop("devices", UNSET)
        devices: Union[Unset, DevicesRoot]
        if isinstance(_devices, Unset):
            devices = UNSET
        else:
            devices = DevicesRoot.from_dict(_devices)

        ephemeral = d.pop("ephemeral", UNSET)

        _expanded_config = d.pop("expanded_config", UNSET)
        expanded_config: Union[Unset, ExpandedConfig]
        if isinstance(_expanded_config, Unset):
            expanded_config = UNSET
        else:
            expanded_config = ExpandedConfig.from_dict(_expanded_config)

        _expanded_devices = d.pop("expanded_devices", UNSET)
        expanded_devices: Union[Unset, ExpandedDevices]
        if isinstance(_expanded_devices, Unset):
            expanded_devices = UNSET
        else:
            expanded_devices = ExpandedDevices.from_dict(_expanded_devices)

        last_used_at = d.pop("last_used_at", UNSET)

        name = d.pop("name", UNSET)

        profiles = cast(List[str], d.pop("profiles", UNSET))

        stateful = d.pop("stateful", UNSET)

        status = d.pop("status", UNSET)

        status_code = d.pop("status_code", UNSET)

        get_instances_by_name_response = cls(
            architecture=architecture,
            config=config,
            created_at=created_at,
            devices=devices,
            ephemeral=ephemeral,
            expanded_config=expanded_config,
            expanded_devices=expanded_devices,
            last_used_at=last_used_at,
            name=name,
            profiles=profiles,
            stateful=stateful,
            status=status,
            status_code=status_code,
        )

        get_instances_by_name_response.additional_properties = d
        return get_instances_by_name_response

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
