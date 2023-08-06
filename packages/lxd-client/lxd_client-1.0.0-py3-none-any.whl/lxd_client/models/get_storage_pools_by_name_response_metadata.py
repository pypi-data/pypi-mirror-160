from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.disk_config import DiskConfig
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetStoragePoolsByNameResponseMetadata")


@attr.s(auto_attribs=True)
class GetStoragePoolsByNameResponseMetadata:
    """
    Attributes:
        name (Union[Unset, str]):  Example: default.
        driver (Union[Unset, str]):  Example: zfs.
        used_by (Union[Unset, List[str]]):  Example: ['/1.0/instances/alp1', '/1.0/instances/alp10',
            '/1.0/instances/alp11', '/1.0/instances/alp12', '/1.0/instances/alp13', '/1.0/instances/alp14',
            '/1.0/instances/alp15', '/1.0/instances/alp16', '/1.0/instances/alp17', '/1.0/instances/alp18',
            '/1.0/instances/alp19', '/1.0/instances/alp2', '/1.0/instances/alp20', '/1.0/instances/alp3',
            '/1.0/instances/alp4', '/1.0/instances/alp5', '/1.0/instances/alp6', '/1.0/instances/alp7',
            '/1.0/instances/alp8', '/1.0/instances/alp9',
            '/1.0/images/62e850a334bb9d99cac00b2e618e0291e5e7bb7db56c4246ecaf8e46fa0631a6'].
        config (Union[Unset, DiskConfig]):
    """

    name: Union[Unset, str] = UNSET
    driver: Union[Unset, str] = UNSET
    used_by: Union[Unset, List[str]] = UNSET
    config: Union[Unset, DiskConfig] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        driver = self.driver
        used_by: Union[Unset, List[str]] = UNSET
        if not isinstance(self.used_by, Unset):
            used_by = self.used_by

        config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if driver is not UNSET:
            field_dict["driver"] = driver
        if used_by is not UNSET:
            field_dict["used_by"] = used_by
        if config is not UNSET:
            field_dict["config"] = config

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        driver = d.pop("driver", UNSET)

        used_by = cast(List[str], d.pop("used_by", UNSET))

        _config = d.pop("config", UNSET)
        config: Union[Unset, DiskConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = DiskConfig.from_dict(_config)

        get_storage_pools_by_name_response_metadata = cls(
            name=name,
            driver=driver,
            used_by=used_by,
            config=config,
        )

        get_storage_pools_by_name_response_metadata.additional_properties = d
        return get_storage_pools_by_name_response_metadata

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
