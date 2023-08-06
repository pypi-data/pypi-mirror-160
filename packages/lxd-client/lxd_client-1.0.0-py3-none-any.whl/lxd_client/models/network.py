from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.eth_02 import Eth02
from ..types import UNSET, Unset

T = TypeVar("T", bound="Network")


@attr.s(auto_attribs=True)
class Network:
    """
    Attributes:
        eth0 (Union[Unset, Eth02]):
        lo (Union[Unset, Eth02]):
        lxdbr0 (Union[Unset, Eth02]):
        zt0 (Union[Unset, Eth02]):
    """

    eth0: Union[Unset, Eth02] = UNSET
    lo: Union[Unset, Eth02] = UNSET
    lxdbr0: Union[Unset, Eth02] = UNSET
    zt0: Union[Unset, Eth02] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        eth0: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.eth0, Unset):
            eth0 = self.eth0.to_dict()

        lo: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.lo, Unset):
            lo = self.lo.to_dict()

        lxdbr0: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.lxdbr0, Unset):
            lxdbr0 = self.lxdbr0.to_dict()

        zt0: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.zt0, Unset):
            zt0 = self.zt0.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if eth0 is not UNSET:
            field_dict["eth0"] = eth0
        if lo is not UNSET:
            field_dict["lo"] = lo
        if lxdbr0 is not UNSET:
            field_dict["lxdbr0"] = lxdbr0
        if zt0 is not UNSET:
            field_dict["zt0"] = zt0

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _eth0 = d.pop("eth0", UNSET)
        eth0: Union[Unset, Eth02]
        if isinstance(_eth0, Unset):
            eth0 = UNSET
        else:
            eth0 = Eth02.from_dict(_eth0)

        _lo = d.pop("lo", UNSET)
        lo: Union[Unset, Eth02]
        if isinstance(_lo, Unset):
            lo = UNSET
        else:
            lo = Eth02.from_dict(_lo)

        _lxdbr0 = d.pop("lxdbr0", UNSET)
        lxdbr0: Union[Unset, Eth02]
        if isinstance(_lxdbr0, Unset):
            lxdbr0 = UNSET
        else:
            lxdbr0 = Eth02.from_dict(_lxdbr0)

        _zt0 = d.pop("zt0", UNSET)
        zt0: Union[Unset, Eth02]
        if isinstance(_zt0, Unset):
            zt0 = UNSET
        else:
            zt0 = Eth02.from_dict(_zt0)

        network = cls(
            eth0=eth0,
            lo=lo,
            lxdbr0=lxdbr0,
            zt0=zt0,
        )

        network.additional_properties = d
        return network

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
