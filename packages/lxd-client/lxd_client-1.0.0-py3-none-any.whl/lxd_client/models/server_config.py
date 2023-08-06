from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ServerConfig")


@attr.s(auto_attribs=True)
class ServerConfig:
    """
    Example:
        {'core.https_address': '[::]:8443', 'core.trust_password': 'my-password'}

    Attributes:
        core_trust_password (Union[Unset, str]):  Example: my-password.
        core_https_address (Union[Unset, str]):  Example: [::]:8443.
    """

    core_trust_password: Union[Unset, str] = UNSET
    core_https_address: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        core_trust_password = self.core_trust_password
        core_https_address = self.core_https_address

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if core_trust_password is not UNSET:
            field_dict["core.trust_password"] = core_trust_password
        if core_https_address is not UNSET:
            field_dict["core.https_address"] = core_https_address

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        core_trust_password = d.pop("core.trust_password", UNSET)

        core_https_address = d.pop("core.https_address", UNSET)

        server_config = cls(
            core_trust_password=core_trust_password,
            core_https_address=core_https_address,
        )

        server_config.additional_properties = d
        return server_config

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
