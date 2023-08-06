from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetClusterMembersByNameResponse")


@attr.s(auto_attribs=True)
class GetClusterMembersByNameResponse:
    """
    Example:
        {'server_name': 'lxd1', 'database': True, 'message': 'fully operational', 'url': 'https://10.1.1.101:8443',
            'status': 'Online'}

    Attributes:
        server_name (Union[Unset, str]):  Example: lxd1.
        url (Union[Unset, str]):  Example: https://10.1.1.101:8443.
        database (Union[Unset, bool]):  Example: True.
        status (Union[Unset, str]):  Example: Online.
        message (Union[Unset, str]):  Example: fully operational.
    """

    server_name: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    database: Union[Unset, bool] = UNSET
    status: Union[Unset, str] = UNSET
    message: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        server_name = self.server_name
        url = self.url
        database = self.database
        status = self.status
        message = self.message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if server_name is not UNSET:
            field_dict["server_name"] = server_name
        if url is not UNSET:
            field_dict["url"] = url
        if database is not UNSET:
            field_dict["database"] = database
        if status is not UNSET:
            field_dict["status"] = status
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        server_name = d.pop("server_name", UNSET)

        url = d.pop("url", UNSET)

        database = d.pop("database", UNSET)

        status = d.pop("status", UNSET)

        message = d.pop("message", UNSET)

        get_cluster_members_by_name_response = cls(
            server_name=server_name,
            url=url,
            database=database,
            status=status,
            message=message,
        )

        get_cluster_members_by_name_response.additional_properties = d
        return get_cluster_members_by_name_response

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
