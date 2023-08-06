from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SecurityNestingConfig")


@attr.s(auto_attribs=True)
class SecurityNestingConfig:
    """
    Example:
        {'volatile.last_state.idmap': '[{"Isuid":true,"Isgid":false,"Hostid":100000,"Nsid":0,"Maprange":65536},{"Isuid":
            false,"Isgid":true,"Hostid":100000,"Nsid":0,"Maprange":65536}]', 'security.nesting': 'true',
            'volatile.eth0.hwaddr': '00:16:3e:ec:65:a8', 'volatile.base_image':
            'a49d26ce5808075f5175bf31f5cb90561f5023dcd408da8ac5e834096d46b2d8'}

    Attributes:
        security_nesting (Union[Unset, str]):  Example: true.
        volatile_base_image (Union[Unset, str]):  Example:
            a49d26ce5808075f5175bf31f5cb90561f5023dcd408da8ac5e834096d46b2d8.
        volatile_eth0_hwaddr (Union[Unset, str]):  Example: 00:16:3e:ec:65:a8.
        volatile_last_state_idmap (Union[Unset, str]):  Example: [{"Isuid":true,"Isgid":false,"Hostid":100000,"Nsid":0,"
            Maprange":65536},{"Isuid":false,"Isgid":true,"Hostid":100000,"Nsid":0,"Maprange":65536}].
    """

    security_nesting: Union[Unset, str] = UNSET
    volatile_base_image: Union[Unset, str] = UNSET
    volatile_eth0_hwaddr: Union[Unset, str] = UNSET
    volatile_last_state_idmap: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        security_nesting = self.security_nesting
        volatile_base_image = self.volatile_base_image
        volatile_eth0_hwaddr = self.volatile_eth0_hwaddr
        volatile_last_state_idmap = self.volatile_last_state_idmap

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if security_nesting is not UNSET:
            field_dict["security.nesting"] = security_nesting
        if volatile_base_image is not UNSET:
            field_dict["volatile.base_image"] = volatile_base_image
        if volatile_eth0_hwaddr is not UNSET:
            field_dict["volatile.eth0.hwaddr"] = volatile_eth0_hwaddr
        if volatile_last_state_idmap is not UNSET:
            field_dict["volatile.last_state.idmap"] = volatile_last_state_idmap

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        security_nesting = d.pop("security.nesting", UNSET)

        volatile_base_image = d.pop("volatile.base_image", UNSET)

        volatile_eth0_hwaddr = d.pop("volatile.eth0.hwaddr", UNSET)

        volatile_last_state_idmap = d.pop("volatile.last_state.idmap", UNSET)

        security_nesting_config = cls(
            security_nesting=security_nesting,
            volatile_base_image=volatile_base_image,
            volatile_eth0_hwaddr=volatile_eth0_hwaddr,
            volatile_last_state_idmap=volatile_last_state_idmap,
        )

        security_nesting_config.additional_properties = d
        return security_nesting_config

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
