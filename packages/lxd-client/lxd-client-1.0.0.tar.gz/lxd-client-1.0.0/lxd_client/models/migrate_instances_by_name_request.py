from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="MigrateInstancesByNameRequest")


@attr.s(auto_attribs=True)
class MigrateInstancesByNameRequest:
    """
    Attributes:
        control (Union[Unset, str]):  Example: secret1.
        criu (Union[Unset, str]):  Example: secret2.
        fs (Union[Unset, str]):  Example: secret3.
    """

    control: Union[Unset, str] = UNSET
    criu: Union[Unset, str] = UNSET
    fs: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        control = self.control
        criu = self.criu
        fs = self.fs

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if control is not UNSET:
            field_dict["control"] = control
        if criu is not UNSET:
            field_dict["criu"] = criu
        if fs is not UNSET:
            field_dict["fs"] = fs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        control = d.pop("control", UNSET)

        criu = d.pop("criu", UNSET)

        fs = d.pop("fs", UNSET)

        migrate_instances_by_name_request = cls(
            control=control,
            criu=criu,
            fs=fs,
        )

        migrate_instances_by_name_request.additional_properties = d
        return migrate_instances_by_name_request

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
