from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.aliases import Aliases
from ..models.properties_3 import Properties3
from ..models.source_10 import Source10
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateImagesRequest")


@attr.s(auto_attribs=True)
class CreateImagesRequest:
    """Source image dictionary (transfers a remote image)

    Example:
        {'filename': 'filename', 'aliases': [{'name': 'my-alias', 'description': 'A description'}, {'name': 'my-alias',
            'description': 'A description'}], 'public': True, 'auto_update': True, 'compression_algorithm': 'xz', 'source':
            {'mode': 'pull', 'server': 'https://10.0.2.3:8443', 'protocol': 'lxd', 'certificate': 'PEM certificate',
            'fingerprint': 'SHA256', 'name': 'abc', 'alias': 'ubuntu/devel', 'secret': 'my-secret-string', 'type': 'image',
            'url': 'https://www.some-server.com/image'}, 'properties': {'os': 'Ubuntu'}}

    Attributes:
        aliases (List[Aliases]): Set initial aliases ("image_create_aliases" API extension)
        source (Source10):  Example: {'mode': 'pull', 'server': 'https://10.0.2.3:8443', 'protocol': 'lxd',
            'certificate': 'PEM certificate', 'fingerprint': 'SHA256', 'name': 'abc', 'alias': 'ubuntu/devel', 'secret':
            'my-secret-string', 'type': 'image', 'url': 'https://www.some-server.com/image'}.
        filename (Union[Unset, str]): Used for export (optional) Example: filename.
        public (Union[Unset, bool]): Whether the image can be downloaded by untrusted users (defaults to false) Example:
            True.
        auto_update (Union[Unset, bool]): Whether the image should be auto-updated (optional; defaults to false)
            Example: True.
        properties (Union[Unset, Properties3]):  Example: {'os': 'Ubuntu'}.
        compression_algorithm (Union[Unset, str]): Override the compression algorithm for the image (optional) Example:
            xz.
    """

    aliases: List[Aliases]
    source: Source10
    filename: Union[Unset, str] = UNSET
    public: Union[Unset, bool] = UNSET
    auto_update: Union[Unset, bool] = UNSET
    properties: Union[Unset, Properties3] = UNSET
    compression_algorithm: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        aliases = []
        for aliases_item_data in self.aliases:
            aliases_item = aliases_item_data.to_dict()

            aliases.append(aliases_item)

        source = self.source.to_dict()

        filename = self.filename
        public = self.public
        auto_update = self.auto_update
        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        compression_algorithm = self.compression_algorithm

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "aliases": aliases,
                "source": source,
            }
        )
        if filename is not UNSET:
            field_dict["filename"] = filename
        if public is not UNSET:
            field_dict["public"] = public
        if auto_update is not UNSET:
            field_dict["auto_update"] = auto_update
        if properties is not UNSET:
            field_dict["properties"] = properties
        if compression_algorithm is not UNSET:
            field_dict["compression_algorithm"] = compression_algorithm

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        aliases = []
        _aliases = d.pop("aliases")
        for aliases_item_data in _aliases:
            aliases_item = Aliases.from_dict(aliases_item_data)

            aliases.append(aliases_item)

        source = Source10.from_dict(d.pop("source"))

        filename = d.pop("filename", UNSET)

        public = d.pop("public", UNSET)

        auto_update = d.pop("auto_update", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, Properties3]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = Properties3.from_dict(_properties)

        compression_algorithm = d.pop("compression_algorithm", UNSET)

        create_images_request = cls(
            aliases=aliases,
            source=source,
            filename=filename,
            public=public,
            auto_update=auto_update,
            properties=properties,
            compression_algorithm=compression_algorithm,
        )

        create_images_request.additional_properties = d
        return create_images_request

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
