from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.kvm import Kvm
from ..types import UNSET, Unset

T = TypeVar("T", bound="DevicesKvm")


@attr.s(auto_attribs=True)
class DevicesKvm:
    """
    Example:
        {'kvm': {'path': '/dev/kvm', 'type': 'unix-char'}}

    Attributes:
        kvm (Union[Unset, Kvm]):  Example: {'path': '/dev/kvm', 'type': 'unix-char'}.
    """

    kvm: Union[Unset, Kvm] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kvm: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.kvm, Unset):
            kvm = self.kvm.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if kvm is not UNSET:
            field_dict["kvm"] = kvm

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _kvm = d.pop("kvm", UNSET)
        kvm: Union[Unset, Kvm]
        if isinstance(_kvm, Unset):
            kvm = UNSET
        else:
            kvm = Kvm.from_dict(_kvm)

        devices_kvm = cls(
            kvm=kvm,
        )

        devices_kvm.additional_properties = d
        return devices_kvm

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
