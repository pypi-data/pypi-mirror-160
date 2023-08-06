from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Fds2")


@attr.s(auto_attribs=True)
class Fds2:
    """
    Attributes:
        field_0 (Union[Unset, str]):  Example: f5b6c760c0aa37a6430dd2a00c456430282d89f6e1661a077a926ed1bf3d1c2.
        control (Union[Unset, str]):  Example: f5b6c760c0aa37a6430dd2a00c456430282d89f6e1661a077a926ed1bf3d1c21.
    """

    field_0: Union[Unset, str] = UNSET
    control: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_0 = self.field_0
        control = self.control

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field_0 is not UNSET:
            field_dict["0"] = field_0
        if control is not UNSET:
            field_dict["control"] = control

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        field_0 = d.pop("0", UNSET)

        control = d.pop("control", UNSET)

        fds_2 = cls(
            field_0=field_0,
            control=control,
        )

        fds_2.additional_properties = d
        return fds_2

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
