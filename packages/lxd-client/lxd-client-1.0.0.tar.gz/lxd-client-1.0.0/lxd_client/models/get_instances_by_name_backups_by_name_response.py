from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetInstancesByNameBackupsByNameResponse")


@attr.s(auto_attribs=True)
class GetInstancesByNameBackupsByNameResponse:
    """
    Example:
        {'instance_only': False, 'expiry_date': '2018-04-23T10:16:09.000Z', 'optimized_storage': False, 'name':
            'backupName', 'creation_date': '2018-04-23T10:16:09.000Z'}

    Attributes:
        name (Union[Unset, str]):  Example: backupName.
        creation_date (Union[Unset, str]):  Example: 2018-04-23T10:16:09.000Z.
        expiry_date (Union[Unset, str]):  Example: 2018-04-23T10:16:09.000Z.
        instance_only (Union[Unset, bool]):
        optimized_storage (Union[Unset, bool]):
    """

    name: Union[Unset, str] = UNSET
    creation_date: Union[Unset, str] = UNSET
    expiry_date: Union[Unset, str] = UNSET
    instance_only: Union[Unset, bool] = UNSET
    optimized_storage: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        creation_date = self.creation_date
        expiry_date = self.expiry_date
        instance_only = self.instance_only
        optimized_storage = self.optimized_storage

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if creation_date is not UNSET:
            field_dict["creation_date"] = creation_date
        if expiry_date is not UNSET:
            field_dict["expiry_date"] = expiry_date
        if instance_only is not UNSET:
            field_dict["instance_only"] = instance_only
        if optimized_storage is not UNSET:
            field_dict["optimized_storage"] = optimized_storage

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        creation_date = d.pop("creation_date", UNSET)

        expiry_date = d.pop("expiry_date", UNSET)

        instance_only = d.pop("instance_only", UNSET)

        optimized_storage = d.pop("optimized_storage", UNSET)

        get_instances_by_name_backups_by_name_response = cls(
            name=name,
            creation_date=creation_date,
            expiry_date=expiry_date,
            instance_only=instance_only,
            optimized_storage=optimized_storage,
        )

        get_instances_by_name_backups_by_name_response.additional_properties = d
        return get_instances_by_name_backups_by_name_response

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
