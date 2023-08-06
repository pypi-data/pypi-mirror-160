from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.expanded_devices import ExpandedDevices
from ..models.security_nesting_config import SecurityNestingConfig
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetSnapshotInformationResponse")


@attr.s(auto_attribs=True)
class GetSnapshotInformationResponse:
    """
    Example:
        {'size': 738476032, 'devices': {'root': {'path': '/', 'type': 'disk'}, 'eth0': {'nictype': 'bridged', 'parent':
            'lxdbr0', 'name': 'eth0', 'type': 'nic'}}, 'name': 'blah', 'profiles': 'default', 'created_at':
            '2016-03-08T23:55:08.000Z', 'ephemeral': False, 'expanded_config': {'volatile.last_state.idmap': '[{"Isuid":true
            ,"Isgid":false,"Hostid":100000,"Nsid":0,"Maprange":65536},{"Isuid":false,"Isgid":true,"Hostid":100000,"Nsid":0,"
            Maprange":65536}]', 'security.nesting': 'true', 'volatile.eth0.hwaddr': '00:16:3e:ec:65:a8',
            'volatile.base_image': 'a49d26ce5808075f5175bf31f5cb90561f5023dcd408da8ac5e834096d46b2d8'}, 'expanded_devices':
            {'root': {'path': '/', 'type': 'disk'}, 'eth0': {'nictype': 'bridged', 'parent': 'lxdbr0', 'name': 'eth0',
            'type': 'nic'}}, 'config': {'volatile.last_state.idmap': '[{"Isuid":true,"Isgid":false,"Hostid":100000,"Nsid":0,
            "Maprange":65536},{"Isuid":false,"Isgid":true,"Hostid":100000,"Nsid":0,"Maprange":65536}]', 'security.nesting':
            'true', 'volatile.eth0.hwaddr': '00:16:3e:ec:65:a8', 'volatile.base_image':
            'a49d26ce5808075f5175bf31f5cb90561f5023dcd408da8ac5e834096d46b2d8'}, 'stateful': False, 'architecture':
            'x86_64'}

    Attributes:
        architecture (Union[Unset, str]):  Example: x86_64.
        config (Union[Unset, SecurityNestingConfig]):  Example: {'volatile.last_state.idmap': '[{"Isuid":true,"Isgid":fa
            lse,"Hostid":100000,"Nsid":0,"Maprange":65536},{"Isuid":false,"Isgid":true,"Hostid":100000,"Nsid":0,"Maprange":6
            5536}]', 'security.nesting': 'true', 'volatile.eth0.hwaddr': '00:16:3e:ec:65:a8', 'volatile.base_image':
            'a49d26ce5808075f5175bf31f5cb90561f5023dcd408da8ac5e834096d46b2d8'}.
        created_at (Union[Unset, str]):  Example: 2016-03-08T23:55:08.000Z.
        devices (Union[Unset, ExpandedDevices]):  Example: {'root': {'path': '/', 'type': 'disk'}, 'eth0': {'nictype':
            'bridged', 'parent': 'lxdbr0', 'name': 'eth0', 'type': 'nic'}}.
        ephemeral (Union[Unset, bool]):
        expanded_config (Union[Unset, SecurityNestingConfig]):  Example: {'volatile.last_state.idmap': '[{"Isuid":true,"
            Isgid":false,"Hostid":100000,"Nsid":0,"Maprange":65536},{"Isuid":false,"Isgid":true,"Hostid":100000,"Nsid":0,"Ma
            prange":65536}]', 'security.nesting': 'true', 'volatile.eth0.hwaddr': '00:16:3e:ec:65:a8',
            'volatile.base_image': 'a49d26ce5808075f5175bf31f5cb90561f5023dcd408da8ac5e834096d46b2d8'}.
        expanded_devices (Union[Unset, ExpandedDevices]):  Example: {'root': {'path': '/', 'type': 'disk'}, 'eth0':
            {'nictype': 'bridged', 'parent': 'lxdbr0', 'name': 'eth0', 'type': 'nic'}}.
        name (Union[Unset, str]):  Example: blah.
        profiles (Union[Unset, List[str]]):  Example: default.
        size (Union[Unset, float]):  Example: 738476032.
        stateful (Union[Unset, bool]):
    """

    architecture: Union[Unset, str] = UNSET
    config: Union[Unset, SecurityNestingConfig] = UNSET
    created_at: Union[Unset, str] = UNSET
    devices: Union[Unset, ExpandedDevices] = UNSET
    ephemeral: Union[Unset, bool] = UNSET
    expanded_config: Union[Unset, SecurityNestingConfig] = UNSET
    expanded_devices: Union[Unset, ExpandedDevices] = UNSET
    name: Union[Unset, str] = UNSET
    profiles: Union[Unset, List[str]] = UNSET
    size: Union[Unset, float] = UNSET
    stateful: Union[Unset, bool] = UNSET
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

        name = self.name
        profiles: Union[Unset, List[str]] = UNSET
        if not isinstance(self.profiles, Unset):
            profiles = self.profiles

        size = self.size
        stateful = self.stateful

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
        if name is not UNSET:
            field_dict["name"] = name
        if profiles is not UNSET:
            field_dict["profiles"] = profiles
        if size is not UNSET:
            field_dict["size"] = size
        if stateful is not UNSET:
            field_dict["stateful"] = stateful

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        architecture = d.pop("architecture", UNSET)

        _config = d.pop("config", UNSET)
        config: Union[Unset, SecurityNestingConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = SecurityNestingConfig.from_dict(_config)

        created_at = d.pop("created_at", UNSET)

        _devices = d.pop("devices", UNSET)
        devices: Union[Unset, ExpandedDevices]
        if isinstance(_devices, Unset):
            devices = UNSET
        else:
            devices = ExpandedDevices.from_dict(_devices)

        ephemeral = d.pop("ephemeral", UNSET)

        _expanded_config = d.pop("expanded_config", UNSET)
        expanded_config: Union[Unset, SecurityNestingConfig]
        if isinstance(_expanded_config, Unset):
            expanded_config = UNSET
        else:
            expanded_config = SecurityNestingConfig.from_dict(_expanded_config)

        _expanded_devices = d.pop("expanded_devices", UNSET)
        expanded_devices: Union[Unset, ExpandedDevices]
        if isinstance(_expanded_devices, Unset):
            expanded_devices = UNSET
        else:
            expanded_devices = ExpandedDevices.from_dict(_expanded_devices)

        name = d.pop("name", UNSET)

        profiles = cast(List[str], d.pop("profiles", UNSET))

        size = d.pop("size", UNSET)

        stateful = d.pop("stateful", UNSET)

        get_snapshot_information_response = cls(
            architecture=architecture,
            config=config,
            created_at=created_at,
            devices=devices,
            ephemeral=ephemeral,
            expanded_config=expanded_config,
            expanded_devices=expanded_devices,
            name=name,
            profiles=profiles,
            size=size,
            stateful=stateful,
        )

        get_snapshot_information_response.additional_properties = d
        return get_snapshot_information_response

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
