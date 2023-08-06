from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.network_ip_config import NetworkIPConfig
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateNetworksRequest")


@attr.s(auto_attribs=True)
class CreateNetworksRequest:
    """
    Example:
        {'name': 'my-network', 'description': 'My network', 'config': {'ipv4.address': 'none', 'ipv6.nat': 'true',
            'ipv6.address': '2001:470:b368:4242::1/64'}}

    Attributes:
        name (Union[Unset, str]):  Example: my-network.
        description (Union[Unset, str]):  Example: My network.
        config (Union[Unset, NetworkIPConfig]):  Example: {'ipv4.address': 'none', 'ipv6.nat': 'true', 'ipv6.address':
            '2001:470:b368:4242::1/64'}.
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    config: Union[Unset, NetworkIPConfig] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if config is not UNSET:
            field_dict["config"] = config

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        _config = d.pop("config", UNSET)
        config: Union[Unset, NetworkIPConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = NetworkIPConfig.from_dict(_config)

        create_networks_request = cls(
            name=name,
            description=description,
            config=config,
        )

        create_networks_request.additional_properties = d
        return create_networks_request

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
