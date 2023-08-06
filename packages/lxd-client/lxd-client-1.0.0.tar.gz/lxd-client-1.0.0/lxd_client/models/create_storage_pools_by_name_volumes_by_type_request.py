from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.create_storage_pools_by_name_volumes_by_type_request_config import (
    CreateStoragePoolsByNameVolumesByTypeRequestConfig,
)
from ..models.source_13 import Source13
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateStoragePoolsByNameVolumesByTypeRequest")


@attr.s(auto_attribs=True)
class CreateStoragePoolsByNameVolumesByTypeRequest:
    """Input (when copying a volume)

    Example:
        {'name': 'vol1', 'source': {'mode': 'pull', 'pool': 'pool2', 'name': 'vol2', 'type': 'migration'}, 'config': {}}

    Attributes:
        config (Union[Unset, CreateStoragePoolsByNameVolumesByTypeRequestConfig]):
        name (Union[Unset, str]):  Example: vol1.
        source (Union[Unset, Source13]):  Example: {'mode': 'pull', 'pool': 'pool2', 'name': 'vol2', 'type':
            'migration'}.
    """

    config: Union[Unset, CreateStoragePoolsByNameVolumesByTypeRequestConfig] = UNSET
    name: Union[Unset, str] = UNSET
    source: Union[Unset, Source13] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        name = self.name
        source: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config is not UNSET:
            field_dict["config"] = config
        if name is not UNSET:
            field_dict["name"] = name
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _config = d.pop("config", UNSET)
        config: Union[Unset, CreateStoragePoolsByNameVolumesByTypeRequestConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = CreateStoragePoolsByNameVolumesByTypeRequestConfig.from_dict(_config)

        name = d.pop("name", UNSET)

        _source = d.pop("source", UNSET)
        source: Union[Unset, Source13]
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = Source13.from_dict(_source)

        create_storage_pools_by_name_volumes_by_type_request = cls(
            config=config,
            name=name,
            source=source,
        )

        create_storage_pools_by_name_volumes_by_type_request.additional_properties = d
        return create_storage_pools_by_name_volumes_by_type_request

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
