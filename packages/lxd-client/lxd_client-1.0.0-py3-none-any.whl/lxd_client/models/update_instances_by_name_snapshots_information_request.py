from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateInstancesByNameSnapshotsInformationRequest")


@attr.s(auto_attribs=True)
class UpdateInstancesByNameSnapshotsInformationRequest:
    """
    Example:
        {'expires_at': '2019-01-16T10:34:56.000Z'}

    Attributes:
        expires_at (Union[Unset, str]):  Example: 2019-01-16T10:34:56.000Z.
    """

    expires_at: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        expires_at = self.expires_at

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expires_at = d.pop("expires_at", UNSET)

        update_instances_by_name_snapshots_information_request = cls(
            expires_at=expires_at,
        )

        update_instances_by_name_snapshots_information_request.additional_properties = d
        return update_instances_by_name_snapshots_information_request

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
