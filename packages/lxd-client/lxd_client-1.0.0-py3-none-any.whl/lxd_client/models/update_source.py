from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateSource")


@attr.s(auto_attribs=True)
class UpdateSource:
    """
    Example:
        {'server': 'https://10.1.2.4:8443', 'protocol': 'lxd', 'certificate': 'PEM certificate', 'alias':
            'ubuntu/bionic/amd64'}

    Attributes:
        server (Union[Unset, str]):  Example: https://10.1.2.4:8443.
        protocol (Union[Unset, str]):  Example: lxd.
        certificate (Union[Unset, str]):  Example: PEM certificate.
        alias (Union[Unset, str]):  Example: ubuntu/bionic/amd64.
    """

    server: Union[Unset, str] = UNSET
    protocol: Union[Unset, str] = UNSET
    certificate: Union[Unset, str] = UNSET
    alias: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        server = self.server
        protocol = self.protocol
        certificate = self.certificate
        alias = self.alias

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if server is not UNSET:
            field_dict["server"] = server
        if protocol is not UNSET:
            field_dict["protocol"] = protocol
        if certificate is not UNSET:
            field_dict["certificate"] = certificate
        if alias is not UNSET:
            field_dict["alias"] = alias

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        server = d.pop("server", UNSET)

        protocol = d.pop("protocol", UNSET)

        certificate = d.pop("certificate", UNSET)

        alias = d.pop("alias", UNSET)

        update_source = cls(
            server=server,
            protocol=protocol,
            certificate=certificate,
            alias=alias,
        )

        update_source.additional_properties = d
        return update_source

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
