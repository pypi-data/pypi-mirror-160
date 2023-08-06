from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetInstancesByNameBackupsByNameExportResponse")


@attr.s(auto_attribs=True)
class GetInstancesByNameBackupsByNameExportResponse:
    """
    Example:
        {'data': '<byte-stream>'}

    Attributes:
        data (Union[Unset, str]):  Example: <byte-stream>.
    """

    data: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = self.data

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        data = d.pop("data", UNSET)

        get_instances_by_name_backups_by_name_export_response = cls(
            data=data,
        )

        get_instances_by_name_backups_by_name_export_response.additional_properties = d
        return get_instances_by_name_backups_by_name_export_response

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
