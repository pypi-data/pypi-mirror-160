from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.error_response_metadata import ErrorResponseMetadata
from ..types import UNSET, Unset

T = TypeVar("T", bound="ErrorResponse")


@attr.s(auto_attribs=True)
class ErrorResponse:
    """
    Attributes:
        type (Union[Unset, str]):  Example: error.
        error (Union[Unset, str]):  Example: Failure.
        error_code (Union[Unset, int]):  Example: 400.
        metadata (Union[Unset, ErrorResponseMetadata]): More details about the error
    """

    type: Union[Unset, str] = UNSET
    error: Union[Unset, str] = UNSET
    error_code: Union[Unset, int] = UNSET
    metadata: Union[Unset, ErrorResponseMetadata] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        error = self.error
        error_code = self.error_code
        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if error is not UNSET:
            field_dict["error"] = error
        if error_code is not UNSET:
            field_dict["error_code"] = error_code
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type", UNSET)

        error = d.pop("error", UNSET)

        error_code = d.pop("error_code", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, ErrorResponseMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ErrorResponseMetadata.from_dict(_metadata)

        error_response = cls(
            type=type,
            error=error,
            error_code=error_code,
            metadata=metadata,
        )

        error_response.additional_properties = d
        return error_response

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
