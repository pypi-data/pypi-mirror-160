from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Memory")


@attr.s(auto_attribs=True)
class Memory:
    """
    Attributes:
        usage (Union[Unset, float]):  Example: 51126272.
        usage_peak (Union[Unset, float]):  Example: 70246400.
        swap_usage (Union[Unset, float]):
        swap_usage_peak (Union[Unset, float]):
    """

    usage: Union[Unset, float] = UNSET
    usage_peak: Union[Unset, float] = UNSET
    swap_usage: Union[Unset, float] = UNSET
    swap_usage_peak: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        usage = self.usage
        usage_peak = self.usage_peak
        swap_usage = self.swap_usage
        swap_usage_peak = self.swap_usage_peak

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if usage is not UNSET:
            field_dict["usage"] = usage
        if usage_peak is not UNSET:
            field_dict["usage_peak"] = usage_peak
        if swap_usage is not UNSET:
            field_dict["swap_usage"] = swap_usage
        if swap_usage_peak is not UNSET:
            field_dict["swap_usage_peak"] = swap_usage_peak

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        usage = d.pop("usage", UNSET)

        usage_peak = d.pop("usage_peak", UNSET)

        swap_usage = d.pop("swap_usage", UNSET)

        swap_usage_peak = d.pop("swap_usage_peak", UNSET)

        memory = cls(
            usage=usage,
            usage_peak=usage_peak,
            swap_usage=swap_usage,
            swap_usage_peak=swap_usage_peak,
        )

        memory.additional_properties = d
        return memory

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
