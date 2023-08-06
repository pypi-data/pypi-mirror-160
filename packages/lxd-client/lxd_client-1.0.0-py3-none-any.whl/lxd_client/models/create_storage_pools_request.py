from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.size_config import SizeConfig
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateStoragePoolsRequest")


@attr.s(auto_attribs=True)
class CreateStoragePoolsRequest:
    """
    Example:
        {'driver': 'zfs', 'name': 'pool1', 'config': {'size': '10GB'}}

    Attributes:
        config (Union[Unset, SizeConfig]):  Example: {'size': '10GB'}.
        driver (Union[Unset, str]):  Example: zfs.
        name (Union[Unset, str]):  Example: pool1.
    """

    config: Union[Unset, SizeConfig] = UNSET
    driver: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        driver = self.driver
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config is not UNSET:
            field_dict["config"] = config
        if driver is not UNSET:
            field_dict["driver"] = driver
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _config = d.pop("config", UNSET)
        config: Union[Unset, SizeConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = SizeConfig.from_dict(_config)

        driver = d.pop("driver", UNSET)

        name = d.pop("name", UNSET)

        create_storage_pools_request = cls(
            config=config,
            driver=driver,
            name=name,
        )

        create_storage_pools_request.additional_properties = d
        return create_storage_pools_request

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
