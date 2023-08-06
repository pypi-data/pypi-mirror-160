from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.standard_return_value_response_metadata import StandardReturnValueResponseMetadata
from ..types import UNSET, Unset

T = TypeVar("T", bound="StandardReturnValueResponse")


@attr.s(auto_attribs=True)
class StandardReturnValueResponse:
    """
    Example:
        {'metadata': '{}', 'status_code': 200, 'type': 'sync', 'status': 'Success', 'error': 'Failure', 'error_code':
            400}

    Attributes:
        type (str):  Example: sync.
        status (str): String version of the operation's status Example: Success.
        metadata (StandardReturnValueResponseMetadata):
        status_code (Union[Unset, int]): Integer version of the operation's status (use this rather than status)
            Example: 200.
        error (Union[Unset, str]):  Example: Failure.
        error_code (Union[Unset, int]):  Example: 400.
    """

    type: str
    status: str
    metadata: StandardReturnValueResponseMetadata
    status_code: Union[Unset, int] = UNSET
    error: Union[Unset, str] = UNSET
    error_code: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        status = self.status
        metadata = self.metadata.to_dict()

        status_code = self.status_code
        error = self.error
        error_code = self.error_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "status": status,
                "metadata": metadata,
            }
        )
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if error is not UNSET:
            field_dict["error"] = error
        if error_code is not UNSET:
            field_dict["error_code"] = error_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type")

        status = d.pop("status")

        metadata = StandardReturnValueResponseMetadata.from_dict(d.pop("metadata"))

        status_code = d.pop("status_code", UNSET)

        error = d.pop("error", UNSET)

        error_code = d.pop("error_code", UNSET)

        standard_return_value_response = cls(
            type=type,
            status=status,
            metadata=metadata,
            status_code=status_code,
            error=error,
            error_code=error_code,
        )

        standard_return_value_response.additional_properties = d
        return standard_return_value_response

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
