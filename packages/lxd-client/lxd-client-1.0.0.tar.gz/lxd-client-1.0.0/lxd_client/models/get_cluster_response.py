from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.member_config import MemberConfig
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetClusterResponse")


@attr.s(auto_attribs=True)
class GetClusterResponse:
    """
    Example:
        {'server_name': 'node1', 'member_config': [{'name': 'local', 'description': '"source" property for storage pool
            "local"', 'entity': 'storage-pool', 'key': 'source'}, {'name': 'local', 'description': '"source" property for
            storage pool "local"', 'entity': 'storage-pool', 'key': 'source'}], 'enabled': True}

    Attributes:
        server_name (Union[Unset, str]):  Example: node1.
        enabled (Union[Unset, bool]):  Example: True.
        member_config (Union[Unset, List[MemberConfig]]):
    """

    server_name: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    member_config: Union[Unset, List[MemberConfig]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        server_name = self.server_name
        enabled = self.enabled
        member_config: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.member_config, Unset):
            member_config = []
            for member_config_item_data in self.member_config:
                member_config_item = member_config_item_data.to_dict()

                member_config.append(member_config_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if server_name is not UNSET:
            field_dict["server_name"] = server_name
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if member_config is not UNSET:
            field_dict["member_config"] = member_config

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        server_name = d.pop("server_name", UNSET)

        enabled = d.pop("enabled", UNSET)

        member_config = []
        _member_config = d.pop("member_config", UNSET)
        for member_config_item_data in _member_config or []:
            member_config_item = MemberConfig.from_dict(member_config_item_data)

            member_config.append(member_config_item)

        get_cluster_response = cls(
            server_name=server_name,
            enabled=enabled,
            member_config=member_config,
        )

        get_cluster_response.additional_properties = d
        return get_cluster_response

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
