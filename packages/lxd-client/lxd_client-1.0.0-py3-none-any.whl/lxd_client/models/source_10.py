from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Source10")


@attr.s(auto_attribs=True)
class Source10:
    """
    Example:
        {'mode': 'pull', 'server': 'https://10.0.2.3:8443', 'protocol': 'lxd', 'certificate': 'PEM certificate',
            'fingerprint': 'SHA256', 'name': 'abc', 'alias': 'ubuntu/devel', 'secret': 'my-secret-string', 'type': 'image',
            'url': 'https://www.some-server.com/image'}

    Attributes:
        type (str):  Example: image.
        mode (str): Only pull is supported for now Example: pull.
        server (str): Remote server (pull mode only) Example: https://10.0.2.3:8443.
        protocol (str): Protocol (one of lxd or simplestreams, defaults to lxd) Example: lxd.
        secret (str): Secret (pull mode only, private images only) Example: my-secret-string.
        fingerprint (str): Fingerprint of the image (must be set if alias isn't) Example: SHA256.
        alias (str): Name of the alias (must be set if fingerprint isn't) Example: ubuntu/devel.
        certificate (Union[Unset, str]): Optional PEM certificate. If not mentioned, system CA is used. Example: PEM
            certificate.
        name (Union[Unset, str]):  Example: abc.
        url (Union[Unset, str]): URL for the image Example: https://www.some-server.com/image.
    """

    type: str
    mode: str
    server: str
    protocol: str
    secret: str
    fingerprint: str
    alias: str
    certificate: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        mode = self.mode
        server = self.server
        protocol = self.protocol
        secret = self.secret
        fingerprint = self.fingerprint
        alias = self.alias
        certificate = self.certificate
        name = self.name
        url = self.url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "mode": mode,
                "server": server,
                "protocol": protocol,
                "secret": secret,
                "fingerprint": fingerprint,
                "alias": alias,
            }
        )
        if certificate is not UNSET:
            field_dict["certificate"] = certificate
        if name is not UNSET:
            field_dict["name"] = name
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type")

        mode = d.pop("mode")

        server = d.pop("server")

        protocol = d.pop("protocol")

        secret = d.pop("secret")

        fingerprint = d.pop("fingerprint")

        alias = d.pop("alias")

        certificate = d.pop("certificate", UNSET)

        name = d.pop("name", UNSET)

        url = d.pop("url", UNSET)

        source_10 = cls(
            type=type,
            mode=mode,
            server=server,
            protocol=protocol,
            secret=secret,
            fingerprint=fingerprint,
            alias=alias,
            certificate=certificate,
            name=name,
            url=url,
        )

        source_10.additional_properties = d
        return source_10

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
