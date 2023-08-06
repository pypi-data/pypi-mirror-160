from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="MemberConfig2")


@attr.s(auto_attribs=True)
class MemberConfig2:
    """
    Example:
        {'name': 'local', 'value': '/dev/sdb', 'entity': 'storage-pool', 'key': 'source'}

    Attributes:
        entity (Union[Unset, str]):  Example: storage-pool.
        name (Union[Unset, str]):  Example: local.
        key (Union[Unset, str]):  Example: source.
        value (Union[Unset, str]):  Example: /dev/sdb.
    """

    entity: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        entity = self.entity
        name = self.name
        key = self.key
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if entity is not UNSET:
            field_dict["entity"] = entity
        if name is not UNSET:
            field_dict["name"] = name
        if key is not UNSET:
            field_dict["key"] = key
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entity = d.pop("entity", UNSET)

        name = d.pop("name", UNSET)

        key = d.pop("key", UNSET)

        value = d.pop("value", UNSET)

        member_config_2 = cls(
            entity=entity,
            name=name,
            key=key,
            value=value,
        )

        member_config_2.additional_properties = d
        return member_config_2

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
