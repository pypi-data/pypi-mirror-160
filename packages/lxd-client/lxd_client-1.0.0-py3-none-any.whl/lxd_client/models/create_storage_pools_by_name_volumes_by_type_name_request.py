from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateStoragePoolsByNameVolumesByTypeNameRequest")


@attr.s(auto_attribs=True)
class CreateStoragePoolsByNameVolumesByTypeNameRequest:
    """Input (migration across lxd instances)

    Example:
        {'name': 'vol1', 'pool': 'pool13', 'migration': True}

    Attributes:
        name (Union[Unset, str]):  Example: vol1.
        pool (Union[Unset, str]):  Example: pool13.
        migration (Union[Unset, bool]):  Example: True.
    """

    name: Union[Unset, str] = UNSET
    pool: Union[Unset, str] = UNSET
    migration: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        pool = self.pool
        migration = self.migration

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if pool is not UNSET:
            field_dict["pool"] = pool
        if migration is not UNSET:
            field_dict["migration"] = migration

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        pool = d.pop("pool", UNSET)

        migration = d.pop("migration", UNSET)

        create_storage_pools_by_name_volumes_by_type_name_request = cls(
            name=name,
            pool=pool,
            migration=migration,
        )

        create_storage_pools_by_name_volumes_by_type_name_request.additional_properties = d
        return create_storage_pools_by_name_volumes_by_type_name_request

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
