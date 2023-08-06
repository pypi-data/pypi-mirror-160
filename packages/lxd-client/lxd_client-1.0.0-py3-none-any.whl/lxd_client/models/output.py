from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Output")


@attr.s(auto_attribs=True)
class Output:
    """
    Attributes:
        field_1 (Union[Unset, str]):  Example:
            /1.0/instances/example/logs/exec_b0f737b4-2c8a-4edf-a7c1-4cc7e4e9e155.stdout.
        field_2 (Union[Unset, str]):  Example:
            /1.0/instances/example/logs/exec_b0f737b4-2c8a-4edf-a7c1-4cc7e4e9e155.stderr.
    """

    field_1: Union[Unset, str] = UNSET
    field_2: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_1 = self.field_1
        field_2 = self.field_2

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field_1 is not UNSET:
            field_dict["1"] = field_1
        if field_2 is not UNSET:
            field_dict["2"] = field_2

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        field_1 = d.pop("1", UNSET)

        field_2 = d.pop("2", UNSET)

        output = cls(
            field_1=field_1,
            field_2=field_2,
        )

        output.additional_properties = d
        return output

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
