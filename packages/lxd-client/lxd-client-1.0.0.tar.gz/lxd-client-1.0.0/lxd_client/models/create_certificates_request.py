from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateCertificatesRequest")


@attr.s(auto_attribs=True)
class CreateCertificatesRequest:
    """
    Example:
        {'password': 'server-trust-password', 'certificate': 'PEM certificate', 'name': 'foo', 'type': 'client'}

    Attributes:
        type (Union[Unset, str]): Certificate type (keyring), currently only client Example: client.
        certificate (Union[Unset, str]): If provided, a valid x509 certificate. If not, the client certificate of the
            connection will be used Example: PEM certificate.
        name (Union[Unset, str]): An optional name for the certificate. If nothing is provided, the host in the TLS
            header for the request is used. Example: foo.
        password (Union[Unset, str]): The trust password for that server (only required if untrusted) Example: server-
            trust-password.
    """

    type: Union[Unset, str] = UNSET
    certificate: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    password: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        certificate = self.certificate
        name = self.name
        password = self.password

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if certificate is not UNSET:
            field_dict["certificate"] = certificate
        if name is not UNSET:
            field_dict["name"] = name
        if password is not UNSET:
            field_dict["password"] = password

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type", UNSET)

        certificate = d.pop("certificate", UNSET)

        name = d.pop("name", UNSET)

        password = d.pop("password", UNSET)

        create_certificates_request = cls(
            type=type,
            certificate=certificate,
            name=name,
            password=password,
        )

        create_certificates_request.additional_properties = d
        return create_certificates_request

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
