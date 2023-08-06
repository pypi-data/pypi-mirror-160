from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.aliases import Aliases
from ..models.properties import Properties
from ..models.update_source import UpdateSource
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetImagesFingerprintResponse")


@attr.s(auto_attribs=True)
class GetImagesFingerprintResponse:
    """
    Example:
        {'aliases': [{'name': 'my-alias', 'description': 'A description'}, {'name': 'my-alias', 'description': 'A
            description'}], 'created_at': '2016-02-01T21:07:41.000Z', 'update_source': {'server': 'https://10.1.2.4:8443',
            'protocol': 'lxd', 'certificate': 'PEM certificate', 'alias': 'ubuntu/bionic/amd64'}, 'last_used_at':
            '1970-01-01T00:00:00.000Z', 'filename': 'ubuntu-bionic-18.04-amd64-server-20180201.tar.xz', 'expires_at':
            '1970-01-01T00:00:00.000Z', 'auto_update': True, 'public': False, 'size': 123792592, 'uploaded_at':
            '2016-02-16T00:44:47.000Z', 'cached': False, 'fingerprint':
            '54c8caac1f61901ed86c68f24af5f5d3672bdc62c71d04f06df3a59e95684473', 'properties': {'os': 'ubuntu', 'release':
            '18.04', 'architecture': 'x86_64'}, 'architecture': 'x86_64'}

    Attributes:
        aliases (Union[Unset, List[Aliases]]):
        architecture (Union[Unset, str]):  Example: x86_64.
        auto_update (Union[Unset, bool]):  Example: True.
        cached (Union[Unset, bool]):
        fingerprint (Union[Unset, str]):  Example: 54c8caac1f61901ed86c68f24af5f5d3672bdc62c71d04f06df3a59e95684473.
        filename (Union[Unset, str]):  Example: ubuntu-bionic-18.04-amd64-server-20180201.tar.xz.
        properties (Union[Unset, Properties]):  Example: {'os': 'ubuntu', 'release': '18.04', 'architecture': 'x86_64'}.
        update_source (Union[Unset, UpdateSource]):  Example: {'server': 'https://10.1.2.4:8443', 'protocol': 'lxd',
            'certificate': 'PEM certificate', 'alias': 'ubuntu/bionic/amd64'}.
        public (Union[Unset, bool]):
        size (Union[Unset, float]):  Example: 123792592.
        created_at (Union[Unset, str]):  Example: 2016-02-01T21:07:41.000Z.
        expires_at (Union[Unset, str]):  Example: 1970-01-01T00:00:00.000Z.
        last_used_at (Union[Unset, str]):  Example: 1970-01-01T00:00:00.000Z.
        uploaded_at (Union[Unset, str]):  Example: 2016-02-16T00:44:47.000Z.
    """

    aliases: Union[Unset, List[Aliases]] = UNSET
    architecture: Union[Unset, str] = UNSET
    auto_update: Union[Unset, bool] = UNSET
    cached: Union[Unset, bool] = UNSET
    fingerprint: Union[Unset, str] = UNSET
    filename: Union[Unset, str] = UNSET
    properties: Union[Unset, Properties] = UNSET
    update_source: Union[Unset, UpdateSource] = UNSET
    public: Union[Unset, bool] = UNSET
    size: Union[Unset, float] = UNSET
    created_at: Union[Unset, str] = UNSET
    expires_at: Union[Unset, str] = UNSET
    last_used_at: Union[Unset, str] = UNSET
    uploaded_at: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        aliases: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.aliases, Unset):
            aliases = []
            for aliases_item_data in self.aliases:
                aliases_item = aliases_item_data.to_dict()

                aliases.append(aliases_item)

        architecture = self.architecture
        auto_update = self.auto_update
        cached = self.cached
        fingerprint = self.fingerprint
        filename = self.filename
        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        update_source: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.update_source, Unset):
            update_source = self.update_source.to_dict()

        public = self.public
        size = self.size
        created_at = self.created_at
        expires_at = self.expires_at
        last_used_at = self.last_used_at
        uploaded_at = self.uploaded_at

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if aliases is not UNSET:
            field_dict["aliases"] = aliases
        if architecture is not UNSET:
            field_dict["architecture"] = architecture
        if auto_update is not UNSET:
            field_dict["auto_update"] = auto_update
        if cached is not UNSET:
            field_dict["cached"] = cached
        if fingerprint is not UNSET:
            field_dict["fingerprint"] = fingerprint
        if filename is not UNSET:
            field_dict["filename"] = filename
        if properties is not UNSET:
            field_dict["properties"] = properties
        if update_source is not UNSET:
            field_dict["update_source"] = update_source
        if public is not UNSET:
            field_dict["public"] = public
        if size is not UNSET:
            field_dict["size"] = size
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if last_used_at is not UNSET:
            field_dict["last_used_at"] = last_used_at
        if uploaded_at is not UNSET:
            field_dict["uploaded_at"] = uploaded_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        aliases = []
        _aliases = d.pop("aliases", UNSET)
        for aliases_item_data in _aliases or []:
            aliases_item = Aliases.from_dict(aliases_item_data)

            aliases.append(aliases_item)

        architecture = d.pop("architecture", UNSET)

        auto_update = d.pop("auto_update", UNSET)

        cached = d.pop("cached", UNSET)

        fingerprint = d.pop("fingerprint", UNSET)

        filename = d.pop("filename", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, Properties]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = Properties.from_dict(_properties)

        _update_source = d.pop("update_source", UNSET)
        update_source: Union[Unset, UpdateSource]
        if isinstance(_update_source, Unset):
            update_source = UNSET
        else:
            update_source = UpdateSource.from_dict(_update_source)

        public = d.pop("public", UNSET)

        size = d.pop("size", UNSET)

        created_at = d.pop("created_at", UNSET)

        expires_at = d.pop("expires_at", UNSET)

        last_used_at = d.pop("last_used_at", UNSET)

        uploaded_at = d.pop("uploaded_at", UNSET)

        get_images_fingerprint_response = cls(
            aliases=aliases,
            architecture=architecture,
            auto_update=auto_update,
            cached=cached,
            fingerprint=fingerprint,
            filename=filename,
            properties=properties,
            update_source=update_source,
            public=public,
            size=size,
            created_at=created_at,
            expires_at=expires_at,
            last_used_at=last_used_at,
            uploaded_at=uploaded_at,
        )

        get_images_fingerprint_response.additional_properties = d
        return get_images_fingerprint_response

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
