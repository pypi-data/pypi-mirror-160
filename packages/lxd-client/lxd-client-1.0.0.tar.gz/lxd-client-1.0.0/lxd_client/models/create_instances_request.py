from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.devices_kvm import DevicesKvm
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateInstancesRequest")


@attr.s(auto_attribs=True)
class CreateInstancesRequest:
    """
    Example:
        {'devices': {'kvm': {'path': '/dev/kvm', 'type': 'unix-char'}}, 'name': 'my-new-instance', 'profiles':
            ['default'], 'ephemeral': True, 'source': {'instance_only': True, 'server': 'https://10.0.2.3:8443',
            'certificate': 'PEM certificate', 'secret': 'my-secret-string', 'source': 'my-old-instance', 'type': 'image',
            'secrets': {'criu': 'my-other-secret', 'control': 'my-secret-string', 'fs': 'my third secret'}, 'mode': 'pull',
            'protocol': 'lxd', 'base-image': '<fingerprint>', 'fingerprint': 'SHA-256', 'alias': 'ubuntu/devel',
            'operation': 'https://10.0.2.3:8443/1.0/operations/<UUID>', 'properties': {'os': 'ubuntu', 'release': '18.04',
            'architecture': 'x86_64'}, 'live': True}, 'type': 'container', 'config': {'limits.cpu': '2'}, 'instance_type':
            'c2.micro', 'architecture': 'x86_64'}

    Attributes:
        name (str): 64 chars max, ASCII, no slash, no colon and no comma Example: my-new-instance.
        architecture (str):  Example: x86_64.
        profiles (List[str]): List of profiles Example: ['default'].
        ephemeral (bool): Whether to destroy the instance on shutdown Example: True.
        config (Any): This is a map of config parameters to be used during instance creation. The keys for this map are
            the keys from instance.md file (https://github.com/lxc/lxd/blob/master/doc/instances.md#keyvalue-configuration)
            and values are the fields to set. Example: {'limits.cpu': '2', 'limits.memory': '512MB'}.
        source (Any): Source to be used to create this container.
            Can be: "image", "migration", "copy" or "none" Example: {'type': 'image', 'fingerprint':
            '6d825770a54383a01cdb78ae1c66260024629bb3b362f0ecd7b74dfcc8aa435f'}.
        type (Union[Unset, str]): Optional. Can be "virtual-machine", "container" - by default it set to "container"
            Example: container.
        devices (Union[Unset, DevicesKvm]):  Example: {'kvm': {'path': '/dev/kvm', 'type': 'unix-char'}}.
        instance_type (Union[Unset, str]): An optional instance type to use as basis for limits Example: c2.micro.
    """

    name: str
    architecture: str
    profiles: List[str]
    ephemeral: bool
    config: Any
    source: Any
    type: Union[Unset, str] = UNSET
    devices: Union[Unset, DevicesKvm] = UNSET
    instance_type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        architecture = self.architecture
        profiles = self.profiles

        ephemeral = self.ephemeral
        config = self.config
        source = self.source
        type = self.type
        devices: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.devices, Unset):
            devices = self.devices.to_dict()

        instance_type = self.instance_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "architecture": architecture,
                "profiles": profiles,
                "ephemeral": ephemeral,
                "config": config,
                "source": source,
            }
        )
        if type is not UNSET:
            field_dict["type"] = type
        if devices is not UNSET:
            field_dict["devices"] = devices
        if instance_type is not UNSET:
            field_dict["instance_type"] = instance_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        architecture = d.pop("architecture")

        profiles = cast(List[str], d.pop("profiles"))

        ephemeral = d.pop("ephemeral")

        config = d.pop("config")

        source = d.pop("source")

        type = d.pop("type", UNSET)

        _devices = d.pop("devices", UNSET)
        devices: Union[Unset, DevicesKvm]
        if isinstance(_devices, Unset):
            devices = UNSET
        else:
            devices = DevicesKvm.from_dict(_devices)

        instance_type = d.pop("instance_type", UNSET)

        create_instances_request = cls(
            name=name,
            architecture=architecture,
            profiles=profiles,
            ephemeral=ephemeral,
            config=config,
            source=source,
            type=type,
            devices=devices,
            instance_type=instance_type,
        )

        create_instances_request.additional_properties = d
        return create_instances_request

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
