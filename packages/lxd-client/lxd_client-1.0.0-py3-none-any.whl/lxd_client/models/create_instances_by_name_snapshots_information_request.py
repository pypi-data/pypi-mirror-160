from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateInstancesByNameSnapshotsInformationRequest")


@attr.s(auto_attribs=True)
class CreateInstancesByNameSnapshotsInformationRequest:
    """setup the migration source

    Example:
        {'name': 'new-name', 'migration': True, 'live': 'true'}

    Attributes:
        name (Union[Unset, str]):  Example: new-name.
        migration (Union[Unset, bool]):  Example: True.
        live (Union[Unset, str]):  Example: true.
    """

    name: Union[Unset, str] = UNSET
    migration: Union[Unset, bool] = UNSET
    live: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        migration = self.migration
        live = self.live

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if migration is not UNSET:
            field_dict["migration"] = migration
        if live is not UNSET:
            field_dict["live"] = live

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        migration = d.pop("migration", UNSET)

        live = d.pop("live", UNSET)

        create_instances_by_name_snapshots_information_request = cls(
            name=name,
            migration=migration,
            live=live,
        )

        create_instances_by_name_snapshots_information_request.additional_properties = d
        return create_instances_by_name_snapshots_information_request

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
