from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Source13")


@attr.s(auto_attribs=True)
class Source13:
    """
    Example:
        {'mode': 'pull', 'pool': 'pool2', 'name': 'vol2', 'type': 'migration'}

    Attributes:
        pool (Union[Unset, str]):  Example: pool2.
        name (Union[Unset, str]):  Example: vol2.
        type (Union[Unset, str]):  Example: migration.
        mode (Union[Unset, str]):  Example: pull.
    """

    pool: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    mode: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pool = self.pool
        name = self.name
        type = self.type
        mode = self.mode

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if pool is not UNSET:
            field_dict["pool"] = pool
        if name is not UNSET:
            field_dict["name"] = name
        if type is not UNSET:
            field_dict["type"] = type
        if mode is not UNSET:
            field_dict["mode"] = mode

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pool = d.pop("pool", UNSET)

        name = d.pop("name", UNSET)

        type = d.pop("type", UNSET)

        mode = d.pop("mode", UNSET)

        source_13 = cls(
            pool=pool,
            name=name,
            type=type,
            mode=mode,
        )

        source_13.additional_properties = d
        return source_13

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
