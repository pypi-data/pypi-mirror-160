from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.cpu_2 import Cpu2
from ..models.memory_2 import Memory2
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetResourcesResponseMetadata")


@attr.s(auto_attribs=True)
class GetResourcesResponseMetadata:
    """
    Attributes:
        cpu (Union[Unset, Cpu2]):
        memory (Union[Unset, Memory2]):
    """

    cpu: Union[Unset, Cpu2] = UNSET
    memory: Union[Unset, Memory2] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cpu: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.cpu, Unset):
            cpu = self.cpu.to_dict()

        memory: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.memory, Unset):
            memory = self.memory.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cpu is not UNSET:
            field_dict["cpu"] = cpu
        if memory is not UNSET:
            field_dict["memory"] = memory

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _cpu = d.pop("cpu", UNSET)
        cpu: Union[Unset, Cpu2]
        if isinstance(_cpu, Unset):
            cpu = UNSET
        else:
            cpu = Cpu2.from_dict(_cpu)

        _memory = d.pop("memory", UNSET)
        memory: Union[Unset, Memory2]
        if isinstance(_memory, Unset):
            memory = UNSET
        else:
            memory = Memory2.from_dict(_memory)

        get_resources_response_metadata = cls(
            cpu=cpu,
            memory=memory,
        )

        get_resources_response_metadata.additional_properties = d
        return get_resources_response_metadata

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
