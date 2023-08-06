from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateImagesFingerprintExportRequest")


@attr.s(auto_attribs=True)
class CreateImagesFingerprintExportRequest:
    """
    Example:
        {'aliases': ['alias'], 'certificate': 'target certificate', 'secret': 'secret', 'target': 'target URL'}

    Attributes:
        target (Union[Unset, str]):  Example: target URL.
        secret (Union[Unset, str]):  Example: secret.
        certificate (Union[Unset, str]):  Example: target certificate.
        aliases (Union[Unset, List[str]]):  Example: ['alias'].
    """

    target: Union[Unset, str] = UNSET
    secret: Union[Unset, str] = UNSET
    certificate: Union[Unset, str] = UNSET
    aliases: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        target = self.target
        secret = self.secret
        certificate = self.certificate
        aliases: Union[Unset, List[str]] = UNSET
        if not isinstance(self.aliases, Unset):
            aliases = self.aliases

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if target is not UNSET:
            field_dict["target"] = target
        if secret is not UNSET:
            field_dict["secret"] = secret
        if certificate is not UNSET:
            field_dict["certificate"] = certificate
        if aliases is not UNSET:
            field_dict["aliases"] = aliases

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        target = d.pop("target", UNSET)

        secret = d.pop("secret", UNSET)

        certificate = d.pop("certificate", UNSET)

        aliases = cast(List[str], d.pop("aliases", UNSET))

        create_images_fingerprint_export_request = cls(
            target=target,
            secret=secret,
            certificate=certificate,
            aliases=aliases,
        )

        create_images_fingerprint_export_request.additional_properties = d
        return create_images_fingerprint_export_request

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
