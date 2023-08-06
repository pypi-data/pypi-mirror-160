from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateFingerprintRequest")


@attr.s(auto_attribs=True)
class UpdateFingerprintRequest:
    """
    Example:
        {'name': 'foo', 'type': 'client'}

    Attributes:
        type (Union[Unset, str]): Certificate type (keyring), currently only client Example: client.
        name (Union[Unset, str]): An optional name for the certificate. If nothing is provided, the host in the TLS
            header for the request is used. Example: foo.
    """

    type: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type", UNSET)

        name = d.pop("name", UNSET)

        update_fingerprint_request = cls(
            type=type,
            name=name,
        )

        update_fingerprint_request.additional_properties = d
        return update_fingerprint_request

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
