from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.context import Context
from ..types import UNSET, Unset

T = TypeVar("T", bound="Metadata2")


@attr.s(auto_attribs=True)
class Metadata2:
    """
    Example:
        {'level': 'info', 'context': {'method': 'GET', 'ip': '@', 'url': '/1.0/instances/xen/snapshots'}, 'message':
            'handling'}

    Attributes:
        context (Union[Unset, Context]):  Example: {'method': 'GET', 'ip': '@', 'url': '/1.0/instances/xen/snapshots'}.
        level (Union[Unset, str]):  Example: info.
        message (Union[Unset, str]):  Example: handling.
    """

    context: Union[Unset, Context] = UNSET
    level: Union[Unset, str] = UNSET
    message: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        context: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()

        level = self.level
        message = self.message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if context is not UNSET:
            field_dict["context"] = context
        if level is not UNSET:
            field_dict["level"] = level
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _context = d.pop("context", UNSET)
        context: Union[Unset, Context]
        if isinstance(_context, Unset):
            context = UNSET
        else:
            context = Context.from_dict(_context)

        level = d.pop("level", UNSET)

        message = d.pop("message", UNSET)

        metadata_2 = cls(
            context=context,
            level=level,
            message=message,
        )

        metadata_2.additional_properties = d
        return metadata_2

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
