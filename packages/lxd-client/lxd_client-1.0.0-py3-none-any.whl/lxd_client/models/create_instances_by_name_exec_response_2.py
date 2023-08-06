from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.fds_1 import Fds1
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateInstancesByNameExecResponse2")


@attr.s(auto_attribs=True)
class CreateInstancesByNameExecResponse2:
    """Return (with wait-for-websocket=true and interactive=true)

    Attributes:
        fds (Union[Unset, Fds1]):
    """

    fds: Union[Unset, Fds1] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        fds: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fds, Unset):
            fds = self.fds.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if fds is not UNSET:
            field_dict["fds"] = fds

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _fds = d.pop("fds", UNSET)
        fds: Union[Unset, Fds1]
        if isinstance(_fds, Unset):
            fds = UNSET
        else:
            fds = Fds1.from_dict(_fds)

        create_instances_by_name_exec_response_2 = cls(
            fds=fds,
        )

        create_instances_by_name_exec_response_2.additional_properties = d
        return create_instances_by_name_exec_response_2

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
