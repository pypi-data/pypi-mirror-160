from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Sockets")


@attr.s(auto_attribs=True)
class Sockets:
    """
    Attributes:
        cores (Union[Unset, float]):  Example: 2.
        frequency (Union[Unset, float]):  Example: 2691.
        frequency_turbo (Union[Unset, float]):  Example: 3400.
        name (Union[Unset, str]):  Example: GenuineIntel.
        vendor (Union[Unset, str]):  Example: Intel(R) Core(TM) i5-3340M CPU @ 2.70GHz.
        threads (Union[Unset, float]):  Example: 4.
    """

    cores: Union[Unset, float] = UNSET
    frequency: Union[Unset, float] = UNSET
    frequency_turbo: Union[Unset, float] = UNSET
    name: Union[Unset, str] = UNSET
    vendor: Union[Unset, str] = UNSET
    threads: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cores = self.cores
        frequency = self.frequency
        frequency_turbo = self.frequency_turbo
        name = self.name
        vendor = self.vendor
        threads = self.threads

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cores is not UNSET:
            field_dict["cores"] = cores
        if frequency is not UNSET:
            field_dict["frequency"] = frequency
        if frequency_turbo is not UNSET:
            field_dict["frequency_turbo"] = frequency_turbo
        if name is not UNSET:
            field_dict["name"] = name
        if vendor is not UNSET:
            field_dict["vendor"] = vendor
        if threads is not UNSET:
            field_dict["threads"] = threads

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        cores = d.pop("cores", UNSET)

        frequency = d.pop("frequency", UNSET)

        frequency_turbo = d.pop("frequency_turbo", UNSET)

        name = d.pop("name", UNSET)

        vendor = d.pop("vendor", UNSET)

        threads = d.pop("threads", UNSET)

        sockets = cls(
            cores=cores,
            frequency=frequency,
            frequency_turbo=frequency_turbo,
            name=name,
            vendor=vendor,
            threads=threads,
        )

        sockets.additional_properties = d
        return sockets

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
