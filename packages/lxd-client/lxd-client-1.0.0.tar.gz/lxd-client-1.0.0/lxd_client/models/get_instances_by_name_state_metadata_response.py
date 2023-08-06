from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.cpu import Cpu
from ..models.disk import Disk
from ..models.memory import Memory
from ..models.network import Network
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetInstancesByNameStateMetadataResponse")


@attr.s(auto_attribs=True)
class GetInstancesByNameStateMetadataResponse:
    """
    Attributes:
        status (Union[Unset, str]):  Example: Running.
        status_code (Union[Unset, float]):  Example: 200.
        cpu (Union[Unset, Cpu]):
        disk (Union[Unset, Disk]):
        memory (Union[Unset, Memory]):
        network (Union[Unset, Network]):
        pid (Union[Unset, float]):  Example: 13663.
        processes (Union[Unset, float]):  Example: 32.
    """

    status: Union[Unset, str] = UNSET
    status_code: Union[Unset, float] = UNSET
    cpu: Union[Unset, Cpu] = UNSET
    disk: Union[Unset, Disk] = UNSET
    memory: Union[Unset, Memory] = UNSET
    network: Union[Unset, Network] = UNSET
    pid: Union[Unset, float] = UNSET
    processes: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status
        status_code = self.status_code
        cpu: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.cpu, Unset):
            cpu = self.cpu.to_dict()

        disk: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.disk, Unset):
            disk = self.disk.to_dict()

        memory: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.memory, Unset):
            memory = self.memory.to_dict()

        network: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.network, Unset):
            network = self.network.to_dict()

        pid = self.pid
        processes = self.processes

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if cpu is not UNSET:
            field_dict["cpu"] = cpu
        if disk is not UNSET:
            field_dict["disk"] = disk
        if memory is not UNSET:
            field_dict["memory"] = memory
        if network is not UNSET:
            field_dict["network"] = network
        if pid is not UNSET:
            field_dict["pid"] = pid
        if processes is not UNSET:
            field_dict["processes"] = processes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = d.pop("status", UNSET)

        status_code = d.pop("status_code", UNSET)

        _cpu = d.pop("cpu", UNSET)
        cpu: Union[Unset, Cpu]
        if isinstance(_cpu, Unset):
            cpu = UNSET
        else:
            cpu = Cpu.from_dict(_cpu)

        _disk = d.pop("disk", UNSET)
        disk: Union[Unset, Disk]
        if isinstance(_disk, Unset):
            disk = UNSET
        else:
            disk = Disk.from_dict(_disk)

        _memory = d.pop("memory", UNSET)
        memory: Union[Unset, Memory]
        if isinstance(_memory, Unset):
            memory = UNSET
        else:
            memory = Memory.from_dict(_memory)

        _network = d.pop("network", UNSET)
        network: Union[Unset, Network]
        if isinstance(_network, Unset):
            network = UNSET
        else:
            network = Network.from_dict(_network)

        pid = d.pop("pid", UNSET)

        processes = d.pop("processes", UNSET)

        get_instances_by_name_state_metadata_response = cls(
            status=status,
            status_code=status_code,
            cpu=cpu,
            disk=disk,
            memory=memory,
            network=network,
            pid=pid,
            processes=processes,
        )

        get_instances_by_name_state_metadata_response.additional_properties = d
        return get_instances_by_name_state_metadata_response

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
