from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.sockets import Sockets
from ..types import UNSET, Unset

T = TypeVar("T", bound="Cpu2")


@attr.s(auto_attribs=True)
class Cpu2:
    """
    Attributes:
        sockets (Union[Unset, List[Sockets]]):
        total (Union[Unset, float]):  Example: 2.
    """

    sockets: Union[Unset, List[Sockets]] = UNSET
    total: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        sockets: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.sockets, Unset):
            sockets = []
            for sockets_item_data in self.sockets:
                sockets_item = sockets_item_data.to_dict()

                sockets.append(sockets_item)

        total = self.total

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sockets is not UNSET:
            field_dict["sockets"] = sockets
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        sockets = []
        _sockets = d.pop("sockets", UNSET)
        for sockets_item_data in _sockets or []:
            sockets_item = Sockets.from_dict(sockets_item_data)

            sockets.append(sockets_item)

        total = d.pop("total", UNSET)

        cpu_2 = cls(
            sockets=sockets,
            total=total,
        )

        cpu_2.additional_properties = d
        return cpu_2

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
