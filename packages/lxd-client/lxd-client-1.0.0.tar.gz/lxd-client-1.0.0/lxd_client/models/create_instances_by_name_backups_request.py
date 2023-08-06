from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateInstancesByNameBackupsRequest")


@attr.s(auto_attribs=True)
class CreateInstancesByNameBackupsRequest:
    """
    Example:
        {'instance_only': True, 'optimized_storage': True, 'name': 'backupName', 'expiry': 3600}

    Attributes:
        name (Union[Unset, str]): Unique identifier for the backup Example: backupName.
        expiry (Union[Unset, float]): When to delete the backup automatically Example: 3600.
        instance_only (Union[Unset, bool]): If True, snapshots aren't included Example: True.
        optimized_storage (Union[Unset, bool]): If True, btrfs send or zfs send is used for instance and snapshots
            Example: True.
    """

    name: Union[Unset, str] = UNSET
    expiry: Union[Unset, float] = UNSET
    instance_only: Union[Unset, bool] = UNSET
    optimized_storage: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        expiry = self.expiry
        instance_only = self.instance_only
        optimized_storage = self.optimized_storage

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if expiry is not UNSET:
            field_dict["expiry"] = expiry
        if instance_only is not UNSET:
            field_dict["instance_only"] = instance_only
        if optimized_storage is not UNSET:
            field_dict["optimized_storage"] = optimized_storage

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        expiry = d.pop("expiry", UNSET)

        instance_only = d.pop("instance_only", UNSET)

        optimized_storage = d.pop("optimized_storage", UNSET)

        create_instances_by_name_backups_request = cls(
            name=name,
            expiry=expiry,
            instance_only=instance_only,
            optimized_storage=optimized_storage,
        )

        create_instances_by_name_backups_request.additional_properties = d
        return create_instances_by_name_backups_request

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
