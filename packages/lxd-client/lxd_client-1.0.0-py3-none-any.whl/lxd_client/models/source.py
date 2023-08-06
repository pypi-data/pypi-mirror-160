from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.properties import Properties
from ..models.secrets import Secrets
from ..types import UNSET, Unset

T = TypeVar("T", bound="Source")


@attr.s(auto_attribs=True)
class Source:
    """
    Example:
        {'instance_only': True, 'server': 'https://10.0.2.3:8443', 'certificate': 'PEM certificate', 'secret': 'my-
            secret-string', 'source': 'my-old-instance', 'type': 'image', 'secrets': {'criu': 'my-other-secret', 'control':
            'my-secret-string', 'fs': 'my third secret'}, 'mode': 'pull', 'protocol': 'lxd', 'base-image': '<fingerprint>',
            'fingerprint': 'SHA-256', 'alias': 'ubuntu/devel', 'operation': 'https://10.0.2.3:8443/1.0/operations/<UUID>',
            'properties': {'os': 'ubuntu', 'release': '18.04', 'architecture': 'x86_64'}, 'live': True}

    Attributes:
        type (str): Can be "image", "migration", "copy" or "none". Example: image.
        alias (Union[Unset, str]): Name of the alias. Example: ubuntu/devel.
        fingerprint (Union[Unset, str]): Fingerprint Example: SHA-256.
        properties (Union[Unset, Properties]):  Example: {'os': 'ubuntu', 'release': '18.04', 'architecture': 'x86_64'}.
        mode (Union[Unset, str]): One of "local" (default) or "pull" Example: pull.
        server (Union[Unset, str]): Remote server (pull mode only) Example: https://10.0.2.3:8443.
        protocol (Union[Unset, str]): Protocol (one of lxd or simplestreams, defaults to lxd) Example: lxd.
        certificate (Union[Unset, str]): Optional PEM certificate. If not mentioned, system CA is used. Example: PEM
            certificate.
        secret (Union[Unset, str]): Secret to use to retrieve the image (pull mode only). Example: my-secret-string.
        operation (Union[Unset, str]): Full URL to the remote operation (pull mode only). Example:
            https://10.0.2.3:8443/1.0/operations/<UUID>.
        base_image (Union[Unset, str]): Optional, the base image the instance was created from Example: <fingerprint>.
        instance_only (Union[Unset, bool]): Whether to migrate only the instance without snapshots. Can be "true" or
            "false". Example: True.
        secrets (Union[Unset, Secrets]):  Example: {'criu': 'my-other-secret', 'control': 'my-secret-string', 'fs': 'my
            third secret'}.
        source (Union[Unset, str]): Name of the source instance Example: my-old-instance.
        live (Union[Unset, bool]): Whether migration is performed live Example: True.
    """

    type: str
    alias: Union[Unset, str] = UNSET
    fingerprint: Union[Unset, str] = UNSET
    properties: Union[Unset, Properties] = UNSET
    mode: Union[Unset, str] = UNSET
    server: Union[Unset, str] = UNSET
    protocol: Union[Unset, str] = UNSET
    certificate: Union[Unset, str] = UNSET
    secret: Union[Unset, str] = UNSET
    operation: Union[Unset, str] = UNSET
    base_image: Union[Unset, str] = UNSET
    instance_only: Union[Unset, bool] = UNSET
    secrets: Union[Unset, Secrets] = UNSET
    source: Union[Unset, str] = UNSET
    live: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        alias = self.alias
        fingerprint = self.fingerprint
        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        mode = self.mode
        server = self.server
        protocol = self.protocol
        certificate = self.certificate
        secret = self.secret
        operation = self.operation
        base_image = self.base_image
        instance_only = self.instance_only
        secrets: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.secrets, Unset):
            secrets = self.secrets.to_dict()

        source = self.source
        live = self.live

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )
        if alias is not UNSET:
            field_dict["alias"] = alias
        if fingerprint is not UNSET:
            field_dict["fingerprint"] = fingerprint
        if properties is not UNSET:
            field_dict["properties"] = properties
        if mode is not UNSET:
            field_dict["mode"] = mode
        if server is not UNSET:
            field_dict["server"] = server
        if protocol is not UNSET:
            field_dict["protocol"] = protocol
        if certificate is not UNSET:
            field_dict["certificate"] = certificate
        if secret is not UNSET:
            field_dict["secret"] = secret
        if operation is not UNSET:
            field_dict["operation"] = operation
        if base_image is not UNSET:
            field_dict["base-image"] = base_image
        if instance_only is not UNSET:
            field_dict["instance_only"] = instance_only
        if secrets is not UNSET:
            field_dict["secrets"] = secrets
        if source is not UNSET:
            field_dict["source"] = source
        if live is not UNSET:
            field_dict["live"] = live

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type")

        alias = d.pop("alias", UNSET)

        fingerprint = d.pop("fingerprint", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, Properties]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = Properties.from_dict(_properties)

        mode = d.pop("mode", UNSET)

        server = d.pop("server", UNSET)

        protocol = d.pop("protocol", UNSET)

        certificate = d.pop("certificate", UNSET)

        secret = d.pop("secret", UNSET)

        operation = d.pop("operation", UNSET)

        base_image = d.pop("base-image", UNSET)

        instance_only = d.pop("instance_only", UNSET)

        _secrets = d.pop("secrets", UNSET)
        secrets: Union[Unset, Secrets]
        if isinstance(_secrets, Unset):
            secrets = UNSET
        else:
            secrets = Secrets.from_dict(_secrets)

        source = d.pop("source", UNSET)

        live = d.pop("live", UNSET)

        source = cls(
            type=type,
            alias=alias,
            fingerprint=fingerprint,
            properties=properties,
            mode=mode,
            server=server,
            protocol=protocol,
            certificate=certificate,
            secret=secret,
            operation=operation,
            base_image=base_image,
            instance_only=instance_only,
            secrets=secrets,
            source=source,
            live=live,
        )

        source.additional_properties = d
        return source

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
