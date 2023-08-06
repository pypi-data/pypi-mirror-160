from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Sigusr1SignalRequest")


@attr.s(auto_attribs=True)
class Sigusr1SignalRequest:
    """
    Attributes:
        command (Union[Unset, str]):  Example: signal.
        signal (Union[Unset, int]):  Example: 10.
    """

    command: Union[Unset, str] = UNSET
    signal: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        command = self.command
        signal = self.signal

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if command is not UNSET:
            field_dict["command"] = command
        if signal is not UNSET:
            field_dict["signal"] = signal

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        command = d.pop("command", UNSET)

        signal = d.pop("signal", UNSET)

        sigusr_1_signal_request = cls(
            command=command,
            signal=signal,
        )

        sigusr_1_signal_request.additional_properties = d
        return sigusr_1_signal_request

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
