from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Containers")


@attr.s(auto_attribs=True)
class Containers:
    """
    Attributes:
        containers (Union[Unset, List[str]]):  Example: ['/1.0/instances/test'].
    """

    containers: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        containers: Union[Unset, List[str]] = UNSET
        if not isinstance(self.containers, Unset):
            containers = self.containers

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if containers is not UNSET:
            field_dict["containers"] = containers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        containers = cast(List[str], d.pop("containers", UNSET))

        containers = cls(
            containers=containers,
        )

        containers.additional_properties = d
        return containers

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
