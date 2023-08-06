from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.args import Args
from ..types import UNSET, Unset

T = TypeVar("T", bound="WindowSizeChangeRequest")


@attr.s(auto_attribs=True)
class WindowSizeChangeRequest:
    """Control (window size change)

    Attributes:
        command (Union[Unset, str]):  Example: window-resize.
        args (Union[Unset, Args]):
    """

    command: Union[Unset, str] = UNSET
    args: Union[Unset, Args] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        command = self.command
        args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.args, Unset):
            args = self.args.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if command is not UNSET:
            field_dict["command"] = command
        if args is not UNSET:
            field_dict["args"] = args

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        command = d.pop("command", UNSET)

        _args = d.pop("args", UNSET)
        args: Union[Unset, Args]
        if isinstance(_args, Unset):
            args = UNSET
        else:
            args = Args.from_dict(_args)

        window_size_change_request = cls(
            command=command,
            args=args,
        )

        window_size_change_request.additional_properties = d
        return window_size_change_request

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
