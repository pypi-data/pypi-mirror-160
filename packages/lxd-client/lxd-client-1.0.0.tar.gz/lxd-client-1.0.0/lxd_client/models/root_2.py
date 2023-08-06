from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Root2")


@attr.s(auto_attribs=True)
class Root2:
    """
    Example:
        {'path': '/', 'size': '5GB', 'pool': 'default'}

    Attributes:
        path (Union[Unset, str]):  Example: /.
        pool (Union[Unset, str]):  Example: default.
        size (Union[Unset, str]):  Example: 5GB.
    """

    path: Union[Unset, str] = UNSET
    pool: Union[Unset, str] = UNSET
    size: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        pool = self.pool
        size = self.size

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if path is not UNSET:
            field_dict["path"] = path
        if pool is not UNSET:
            field_dict["pool"] = pool
        if size is not UNSET:
            field_dict["size"] = size

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path", UNSET)

        pool = d.pop("pool", UNSET)

        size = d.pop("size", UNSET)

        root_2 = cls(
            path=path,
            pool=pool,
            size=size,
        )

        root_2.additional_properties = d
        return root_2

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
