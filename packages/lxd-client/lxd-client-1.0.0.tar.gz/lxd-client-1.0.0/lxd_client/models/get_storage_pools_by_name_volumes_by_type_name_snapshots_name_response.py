from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.get_storage_pools_by_name_volumes_by_type_name_snapshots_name_response_config import (
    GetStoragePoolsByNameVolumesByTypeNameSnapshotsNameResponseConfig,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetStoragePoolsByNameVolumesByTypeNameSnapshotsNameResponse")


@attr.s(auto_attribs=True)
class GetStoragePoolsByNameVolumesByTypeNameSnapshotsNameResponse:
    """
    Example:
        {'name': 'snap0', 'description': 'description', 'config': {}}

    Attributes:
        config (Union[Unset, GetStoragePoolsByNameVolumesByTypeNameSnapshotsNameResponseConfig]):
        name (Union[Unset, str]):  Example: snap0.
        description (Union[Unset, str]):
    """

    config: Union[Unset, GetStoragePoolsByNameVolumesByTypeNameSnapshotsNameResponseConfig] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        name = self.name
        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config is not UNSET:
            field_dict["config"] = config
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _config = d.pop("config", UNSET)
        config: Union[Unset, GetStoragePoolsByNameVolumesByTypeNameSnapshotsNameResponseConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = GetStoragePoolsByNameVolumesByTypeNameSnapshotsNameResponseConfig.from_dict(_config)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        get_storage_pools_by_name_volumes_by_type_name_snapshots_name_response = cls(
            config=config,
            name=name,
            description=description,
        )

        get_storage_pools_by_name_volumes_by_type_name_snapshots_name_response.additional_properties = d
        return get_storage_pools_by_name_volumes_by_type_name_snapshots_name_response

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
