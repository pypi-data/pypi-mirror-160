from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetServerStateResponse")


@attr.s(auto_attribs=True)
class GetServerStateResponse:
    """Return value (if trusted)

    Example:
        {'metadata': {'environment': {'architectures': ['x86_64', 'i686'], 'server_pid': 10224, 'storage_version':
            '3.19', 'server': 'lxc', 'addresses': '[1.2.3.4:8443,[1234::1234]:8443]', 'kernel': 'Linux', 'certificate': 'PEM
            certificate', 'storage': 'btrfs', 'server_version': '0.8.1', 'kernel_architecture': 'x86_64', 'driver': 'lxc',
            'kernel_version': '3.16', 'driver_version': '1.0.6'}, 'api_extensions': ['api_extensions', 'api_extensions'],
            'public': False, 'auth': '["guest","untrusted","trusted"]', 'api_status': 'stable', 'api_version': '1.0',
            'config': {'core.https_address': '[::]:8443', 'core.trust_password': True}}}

    Attributes:
        metadata (Union[Unset, Any]):  Example: {'environment': {'architectures': ['x86_64', 'i686'], 'server_pid':
            10224, 'storage_version': '3.19', 'server': 'lxc', 'addresses': '[1.2.3.4:8443,[1234::1234]:8443]', 'kernel':
            'Linux', 'certificate': 'PEM certificate', 'storage': 'btrfs', 'server_version': '0.8.1', 'kernel_architecture':
            'x86_64', 'driver': 'lxc', 'kernel_version': '3.16', 'driver_version': '1.0.6'}, 'api_extensions':
            ['api_extensions', 'api_extensions'], 'public': False, 'auth': '["guest","untrusted","trusted"]', 'api_status':
            'stable', 'api_version': '1.0', 'config': {'core.https_address': '[::]:8443', 'core.trust_password': True}}.
    """

    metadata: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        metadata = self.metadata

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        metadata = d.pop("metadata", UNSET)

        get_server_state_response = cls(
            metadata=metadata,
        )

        get_server_state_response.additional_properties = d
        return get_server_state_response

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
