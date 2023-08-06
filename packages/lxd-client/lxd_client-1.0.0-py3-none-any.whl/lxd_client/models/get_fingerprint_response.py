from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetFingerprintResponse")


@attr.s(auto_attribs=True)
class GetFingerprintResponse:
    """
    Example:
        {'metadata': {'certificate': 'PEM certificate', 'name': 'foo', 'fingerprint': 'SHA256 Hash of the raw
            certificate', 'type': 'client'}}

    Attributes:
        metadata (Union[Unset, Any]):  Example: {'certificate': 'PEM certificate', 'name': 'foo', 'fingerprint': 'SHA256
            Hash of the raw certificate', 'type': 'client'}.
    """

    metadata: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        metadata = self.metadata

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        metadata = d.pop("metadata", UNSET)

        get_fingerprint_response = cls(
            metadata=metadata,
        )

        get_fingerprint_response.additional_properties = d
        return get_fingerprint_response

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
