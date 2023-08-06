from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.output import Output
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateInstancesByNameExecResponse3")


@attr.s(auto_attribs=True)
class CreateInstancesByNameExecResponse3:
    """Return (with interactive=false and record-output=true)

    Attributes:
        fds (Union[Unset, Output]):
        return_ (Union[Unset, int]):
    """

    fds: Union[Unset, Output] = UNSET
    return_: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        fds: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fds, Unset):
            fds = self.fds.to_dict()

        return_ = self.return_

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if fds is not UNSET:
            field_dict["fds"] = fds
        if return_ is not UNSET:
            field_dict["return"] = return_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _fds = d.pop("fds", UNSET)
        fds: Union[Unset, Output]
        if isinstance(_fds, Unset):
            fds = UNSET
        else:
            fds = Output.from_dict(_fds)

        return_ = d.pop("return", UNSET)

        create_instances_by_name_exec_response_3 = cls(
            fds=fds,
            return_=return_,
        )

        create_instances_by_name_exec_response_3.additional_properties = d
        return create_instances_by_name_exec_response_3

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
