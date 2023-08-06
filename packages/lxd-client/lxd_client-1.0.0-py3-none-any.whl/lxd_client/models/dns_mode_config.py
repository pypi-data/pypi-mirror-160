from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DNSModeConfig")


@attr.s(auto_attribs=True)
class DNSModeConfig:
    """
    Example:
        {'dns.mode': 'dynamic'}

    Attributes:
        dns_mode (Union[Unset, str]):  Example: dynamic.
    """

    dns_mode: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        dns_mode = self.dns_mode

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if dns_mode is not UNSET:
            field_dict["dns.mode"] = dns_mode

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dns_mode = d.pop("dns.mode", UNSET)

        dns_mode_config = cls(
            dns_mode=dns_mode,
        )

        dns_mode_config.additional_properties = d
        return dns_mode_config

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
