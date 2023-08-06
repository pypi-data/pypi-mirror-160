from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CpuConfig")


@attr.s(auto_attribs=True)
class CpuConfig:
    """
    Example:
        {'limits.cpu': '3'}

    Attributes:
        limits_cpu (Union[Unset, str]):  Example: 3.
    """

    limits_cpu: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        limits_cpu = self.limits_cpu

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if limits_cpu is not UNSET:
            field_dict["limits.cpu"] = limits_cpu

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        limits_cpu = d.pop("limits.cpu", UNSET)

        cpu_config = cls(
            limits_cpu=limits_cpu,
        )

        cpu_config.additional_properties = d
        return cpu_config

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
