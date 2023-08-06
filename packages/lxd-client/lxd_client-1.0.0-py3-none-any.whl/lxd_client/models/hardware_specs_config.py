from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="HardwareSpecsConfig")


@attr.s(auto_attribs=True)
class HardwareSpecsConfig:
    """
    Example:
        {'limits.cpu': '3', 'volatile.eth0.hwaddr': '00:16:3e:1c:94:38', 'volatile.base_image':
            '97d97a3d1d053840ca19c86cdd0596cf1be060c5157d31407f2a4f9f350c78cc'}

    Attributes:
        limits_cpu (Union[Unset, str]):  Example: 3.
        volatile_base_image (Union[Unset, str]):  Example:
            97d97a3d1d053840ca19c86cdd0596cf1be060c5157d31407f2a4f9f350c78cc.
        volatile_eth0_hwaddr (Union[Unset, str]):  Example: 00:16:3e:1c:94:38.
    """

    limits_cpu: Union[Unset, str] = UNSET
    volatile_base_image: Union[Unset, str] = UNSET
    volatile_eth0_hwaddr: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        limits_cpu = self.limits_cpu
        volatile_base_image = self.volatile_base_image
        volatile_eth0_hwaddr = self.volatile_eth0_hwaddr

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if limits_cpu is not UNSET:
            field_dict["limits.cpu"] = limits_cpu
        if volatile_base_image is not UNSET:
            field_dict["volatile.base_image"] = volatile_base_image
        if volatile_eth0_hwaddr is not UNSET:
            field_dict["volatile.eth0.hwaddr"] = volatile_eth0_hwaddr

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        limits_cpu = d.pop("limits.cpu", UNSET)

        volatile_base_image = d.pop("volatile.base_image", UNSET)

        volatile_eth0_hwaddr = d.pop("volatile.eth0.hwaddr", UNSET)

        hardware_specs_config = cls(
            limits_cpu=limits_cpu,
            volatile_base_image=volatile_base_image,
            volatile_eth0_hwaddr=volatile_eth0_hwaddr,
        )

        hardware_specs_config.additional_properties = d
        return hardware_specs_config

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
