from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.basic_background_operation_response_metadata import BasicBackgroundOperationResponseMetadata
from ..types import UNSET, Unset

T = TypeVar("T", bound="BasicBackgroundOperationResponse")


@attr.s(auto_attribs=True)
class BasicBackgroundOperationResponse:
    """
    Example:
        {'metadata': '{}', 'status_code': 100, 'type': 'async', 'operation': '/1.0/instances/<id>', 'status': 'OK'}

    Attributes:
        type (str):  Example: async.
        status (str): String version of the operation's status Example: OK.
        operation (str): URL to the background operation Example: /1.0/instances/<id>.
        status_code (Union[Unset, int]): Integer version of the operation's status (use this rather than status)
            Example: 100.
        metadata (Union[Unset, BasicBackgroundOperationResponseMetadata]):
    """

    type: str
    status: str
    operation: str
    status_code: Union[Unset, int] = UNSET
    metadata: Union[Unset, BasicBackgroundOperationResponseMetadata] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        status = self.status
        operation = self.operation
        status_code = self.status_code
        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "status": status,
                "operation": operation,
            }
        )
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type")

        status = d.pop("status")

        operation = d.pop("operation")

        status_code = d.pop("status_code", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, BasicBackgroundOperationResponseMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = BasicBackgroundOperationResponseMetadata.from_dict(_metadata)

        basic_background_operation_response = cls(
            type=type,
            status=status,
            operation=operation,
            status_code=status_code,
            metadata=metadata,
        )

        basic_background_operation_response.additional_properties = d
        return basic_background_operation_response

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
