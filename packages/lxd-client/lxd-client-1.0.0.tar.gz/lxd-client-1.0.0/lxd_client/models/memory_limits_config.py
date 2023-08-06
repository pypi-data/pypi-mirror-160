from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="MemoryLimitsConfig")


@attr.s(auto_attribs=True)
class MemoryLimitsConfig:
    """
    Example:
        {'limits.memory': '2GB'}

    Attributes:
        limits_memory (Union[Unset, str]):  Example: 2GB.
    """

    limits_memory: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        limits_memory = self.limits_memory

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if limits_memory is not UNSET:
            field_dict["limits.memory"] = limits_memory

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        limits_memory = d.pop("limits.memory", UNSET)

        memory_limits_config = cls(
            limits_memory=limits_memory,
        )

        memory_limits_config.additional_properties = d
        return memory_limits_config

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
