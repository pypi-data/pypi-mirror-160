from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.member_config_2 import MemberConfig2
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateClusterRequest")


@attr.s(auto_attribs=True)
class UpdateClusterRequest:
    """Input (request to join an existing cluster)

    Example:
        {'server_name': 'node2', 'member_config': [{'name': 'local', 'value': '/dev/sdb', 'entity': 'storage-pool',
            'key': 'source'}, {'name': 'local', 'value': '/dev/sdb', 'entity': 'storage-pool', 'key': 'source'}],
            'cluster_address': '10.1.1.101:8443', 'server_address': '10.1.1.102:8443', 'cluster_certificate': 'BEGIN
            CERTIFICATE-----MIFf-----END CERTIFICATE-----', 'enabled': True, 'cluster_password': 'sekret'}

    Attributes:
        server_name (Union[Unset, str]):  Example: node2.
        server_address (Union[Unset, str]):  Example: 10.1.1.102:8443.
        enabled (Union[Unset, bool]):  Example: True.
        cluster_address (Union[Unset, str]):  Example: 10.1.1.101:8443.
        cluster_certificate (Union[Unset, str]):  Example: BEGIN CERTIFICATE-----MIFf-----END CERTIFICATE-----.
        cluster_password (Union[Unset, str]):  Example: sekret.
        member_config (Union[Unset, List[MemberConfig2]]):
    """

    server_name: Union[Unset, str] = UNSET
    server_address: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    cluster_address: Union[Unset, str] = UNSET
    cluster_certificate: Union[Unset, str] = UNSET
    cluster_password: Union[Unset, str] = UNSET
    member_config: Union[Unset, List[MemberConfig2]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        server_name = self.server_name
        server_address = self.server_address
        enabled = self.enabled
        cluster_address = self.cluster_address
        cluster_certificate = self.cluster_certificate
        cluster_password = self.cluster_password
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
        if server_address is not UNSET:
            field_dict["server_address"] = server_address
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if cluster_address is not UNSET:
            field_dict["cluster_address"] = cluster_address
        if cluster_certificate is not UNSET:
            field_dict["cluster_certificate"] = cluster_certificate
        if cluster_password is not UNSET:
            field_dict["cluster_password"] = cluster_password
        if member_config is not UNSET:
            field_dict["member_config"] = member_config

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        server_name = d.pop("server_name", UNSET)

        server_address = d.pop("server_address", UNSET)

        enabled = d.pop("enabled", UNSET)

        cluster_address = d.pop("cluster_address", UNSET)

        cluster_certificate = d.pop("cluster_certificate", UNSET)

        cluster_password = d.pop("cluster_password", UNSET)

        member_config = []
        _member_config = d.pop("member_config", UNSET)
        for member_config_item_data in _member_config or []:
            member_config_item = MemberConfig2.from_dict(member_config_item_data)

            member_config.append(member_config_item)

        update_cluster_request = cls(
            server_name=server_name,
            server_address=server_address,
            enabled=enabled,
            cluster_address=cluster_address,
            cluster_certificate=cluster_certificate,
            cluster_password=cluster_password,
            member_config=member_config,
        )

        update_cluster_request.additional_properties = d
        return update_cluster_request

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
