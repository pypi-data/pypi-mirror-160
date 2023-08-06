from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Context")


@attr.s(auto_attribs=True)
class Context:
    """
    Example:
        {'method': 'GET', 'ip': '@', 'url': '/1.0/instances/xen/snapshots'}

    Attributes:
        ip (Union[Unset, str]):  Example: @.
        method (Union[Unset, str]):  Example: GET.
        url (Union[Unset, str]):  Example: /1.0/instances/xen/snapshots.
    """

    ip: Union[Unset, str] = UNSET
    method: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        ip = self.ip
        method = self.method
        url = self.url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if ip is not UNSET:
            field_dict["ip"] = ip
        if method is not UNSET:
            field_dict["method"] = method
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        ip = d.pop("ip", UNSET)

        method = d.pop("method", UNSET)

        url = d.pop("url", UNSET)

        context = cls(
            ip=ip,
            method=method,
            url=url,
        )

        context.additional_properties = d
        return context

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
