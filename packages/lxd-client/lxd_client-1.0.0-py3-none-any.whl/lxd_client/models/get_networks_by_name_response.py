from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.network_ip_config import NetworkIPConfig
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetNetworksByNameResponse")


@attr.s(auto_attribs=True)
class GetNetworksByNameResponse:
    """
    Example:
        {'managed': False, 'name': 'lxdbr0', 'type': 'bridge', 'config': {'ipv4.address': 'none', 'ipv6.nat': 'true',
            'ipv6.address': '2001:470:b368:4242::1/64'}, 'used_by': ['/1.0/instances/blah']}

    Attributes:
        config (Union[Unset, NetworkIPConfig]):  Example: {'ipv4.address': 'none', 'ipv6.nat': 'true', 'ipv6.address':
            '2001:470:b368:4242::1/64'}.
        name (Union[Unset, str]):  Example: lxdbr0.
        managed (Union[Unset, bool]):
        type (Union[Unset, str]):  Example: bridge.
        used_by (Union[Unset, List[str]]):  Example: ['/1.0/instances/blah'].
    """

    config: Union[Unset, NetworkIPConfig] = UNSET
    name: Union[Unset, str] = UNSET
    managed: Union[Unset, bool] = UNSET
    type: Union[Unset, str] = UNSET
    used_by: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        name = self.name
        managed = self.managed
        type = self.type
        used_by: Union[Unset, List[str]] = UNSET
        if not isinstance(self.used_by, Unset):
            used_by = self.used_by

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config is not UNSET:
            field_dict["config"] = config
        if name is not UNSET:
            field_dict["name"] = name
        if managed is not UNSET:
            field_dict["managed"] = managed
        if type is not UNSET:
            field_dict["type"] = type
        if used_by is not UNSET:
            field_dict["used_by"] = used_by

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _config = d.pop("config", UNSET)
        config: Union[Unset, NetworkIPConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = NetworkIPConfig.from_dict(_config)

        name = d.pop("name", UNSET)

        managed = d.pop("managed", UNSET)

        type = d.pop("type", UNSET)

        used_by = cast(List[str], d.pop("used_by", UNSET))

        get_networks_by_name_response = cls(
            config=config,
            name=name,
            managed=managed,
            type=type,
            used_by=used_by,
        )

        get_networks_by_name_response.additional_properties = d
        return get_networks_by_name_response

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
