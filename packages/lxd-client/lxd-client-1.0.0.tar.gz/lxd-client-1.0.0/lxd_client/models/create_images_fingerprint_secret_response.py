from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.metadata_3 import Metadata3
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateImagesFingerprintSecretResponse")


@attr.s(auto_attribs=True)
class CreateImagesFingerprintSecretResponse:
    """
    Example:
        {'metadata': {'secret': '52e9ec5885562aa24d05d7b4846ebb8b5f1f7bf5cd6e285639b569d9eaf54c9b'}, 'status_code': 200,
            'type': 'sync', 'status': 'Success'}

    Attributes:
        type (str):  Example: sync.
        status (str): String version of the operation's status Example: Success.
        status_code (Union[Unset, int]): Integer version of the operation's status (use this rather than status)
            Example: 200.
        metadata (Union[Unset, Metadata3]):  Example: {'secret':
            '52e9ec5885562aa24d05d7b4846ebb8b5f1f7bf5cd6e285639b569d9eaf54c9b'}.
    """

    type: str
    status: str
    status_code: Union[Unset, int] = UNSET
    metadata: Union[Unset, Metadata3] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        status = self.status
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

        status_code = d.pop("status_code", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, Metadata3]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata3.from_dict(_metadata)

        create_images_fingerprint_secret_response = cls(
            type=type,
            status=status,
            status_code=status_code,
            metadata=metadata,
        )

        create_images_fingerprint_secret_response.additional_properties = d
        return create_images_fingerprint_secret_response

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
