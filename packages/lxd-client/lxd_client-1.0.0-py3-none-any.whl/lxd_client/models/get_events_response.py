from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.get_events_response_type import GetEventsResponseType
from ..models.metadata_2 import Metadata2
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetEventsResponse")


@attr.s(auto_attribs=True)
class GetEventsResponse:
    """
    Example:
        {'metadata': {'level': 'info', 'context': {'method': 'GET', 'ip': '@', 'url': '/1.0/instances/xen/snapshots'},
            'message': 'handling'}, 'type': 'operation', 'timestamp': '2015-06-10T01:07:24.379Z'}

    Attributes:
        timestamp (Union[Unset, str]): Current timestamp Example: 2015-06-10T01:07:24.379Z.
        type (Union[Unset, GetEventsResponseType]): Notification type Example: operation.
        metadata (Union[Unset, Metadata2]):  Example: {'level': 'info', 'context': {'method': 'GET', 'ip': '@', 'url':
            '/1.0/instances/xen/snapshots'}, 'message': 'handling'}.
    """

    timestamp: Union[Unset, str] = UNSET
    type: Union[Unset, GetEventsResponseType] = UNSET
    metadata: Union[Unset, Metadata2] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        timestamp = self.timestamp
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if type is not UNSET:
            field_dict["type"] = type
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        timestamp = d.pop("timestamp", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, GetEventsResponseType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = GetEventsResponseType(_type)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, Metadata2]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata2.from_dict(_metadata)

        get_events_response = cls(
            timestamp=timestamp,
            type=type,
            metadata=metadata,
        )

        get_events_response.additional_properties = d
        return get_events_response

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
