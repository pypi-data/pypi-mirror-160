from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Environment")


@attr.s(auto_attribs=True)
class Environment:
    """
    Example:
        {'architectures': ['x86_64', 'i686'], 'server_pid': 10224, 'storage_version': '3.19', 'server': 'lxc',
            'addresses': '[1.2.3.4:8443,[1234::1234]:8443]', 'kernel': 'Linux', 'certificate': 'PEM certificate', 'storage':
            'btrfs', 'server_version': '0.8.1', 'kernel_architecture': 'x86_64', 'driver': 'lxc', 'kernel_version': '3.16',
            'driver_version': '1.0.6'}

    Attributes:
        addresses (Union[Unset, List[str]]):  Example: [1.2.3.4:8443,[1234::1234]:8443].
        architectures (Union[Unset, List[str]]):  Example: ['x86_64', 'i686'].
        certificate (Union[Unset, str]):  Example: PEM certificate.
        driver (Union[Unset, str]):  Example: lxc.
        driver_version (Union[Unset, str]):  Example: 1.0.6.
        kernel (Union[Unset, str]):  Example: Linux.
        kernel_architecture (Union[Unset, str]):  Example: x86_64.
        kernel_version (Union[Unset, str]):  Example: 3.16.
        server (Union[Unset, str]):  Example: lxc.
        server_pid (Union[Unset, int]):  Example: 10224.
        server_version (Union[Unset, str]):  Example: 0.8.1.
        storage (Union[Unset, str]):  Example: btrfs.
        storage_version (Union[Unset, str]):  Example: 3.19.
    """

    addresses: Union[Unset, List[str]] = UNSET
    architectures: Union[Unset, List[str]] = UNSET
    certificate: Union[Unset, str] = UNSET
    driver: Union[Unset, str] = UNSET
    driver_version: Union[Unset, str] = UNSET
    kernel: Union[Unset, str] = UNSET
    kernel_architecture: Union[Unset, str] = UNSET
    kernel_version: Union[Unset, str] = UNSET
    server: Union[Unset, str] = UNSET
    server_pid: Union[Unset, int] = UNSET
    server_version: Union[Unset, str] = UNSET
    storage: Union[Unset, str] = UNSET
    storage_version: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        addresses: Union[Unset, List[str]] = UNSET
        if not isinstance(self.addresses, Unset):
            addresses = self.addresses

        architectures: Union[Unset, List[str]] = UNSET
        if not isinstance(self.architectures, Unset):
            architectures = self.architectures

        certificate = self.certificate
        driver = self.driver
        driver_version = self.driver_version
        kernel = self.kernel
        kernel_architecture = self.kernel_architecture
        kernel_version = self.kernel_version
        server = self.server
        server_pid = self.server_pid
        server_version = self.server_version
        storage = self.storage
        storage_version = self.storage_version

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if addresses is not UNSET:
            field_dict["addresses"] = addresses
        if architectures is not UNSET:
            field_dict["architectures"] = architectures
        if certificate is not UNSET:
            field_dict["certificate"] = certificate
        if driver is not UNSET:
            field_dict["driver"] = driver
        if driver_version is not UNSET:
            field_dict["driver_version"] = driver_version
        if kernel is not UNSET:
            field_dict["kernel"] = kernel
        if kernel_architecture is not UNSET:
            field_dict["kernel_architecture"] = kernel_architecture
        if kernel_version is not UNSET:
            field_dict["kernel_version"] = kernel_version
        if server is not UNSET:
            field_dict["server"] = server
        if server_pid is not UNSET:
            field_dict["server_pid"] = server_pid
        if server_version is not UNSET:
            field_dict["server_version"] = server_version
        if storage is not UNSET:
            field_dict["storage"] = storage
        if storage_version is not UNSET:
            field_dict["storage_version"] = storage_version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        addresses = cast(List[str], d.pop("addresses", UNSET))

        architectures = cast(List[str], d.pop("architectures", UNSET))

        certificate = d.pop("certificate", UNSET)

        driver = d.pop("driver", UNSET)

        driver_version = d.pop("driver_version", UNSET)

        kernel = d.pop("kernel", UNSET)

        kernel_architecture = d.pop("kernel_architecture", UNSET)

        kernel_version = d.pop("kernel_version", UNSET)

        server = d.pop("server", UNSET)

        server_pid = d.pop("server_pid", UNSET)

        server_version = d.pop("server_version", UNSET)

        storage = d.pop("storage", UNSET)

        storage_version = d.pop("storage_version", UNSET)

        environment = cls(
            addresses=addresses,
            architectures=architectures,
            certificate=certificate,
            driver=driver,
            driver_version=driver_version,
            kernel=kernel,
            kernel_architecture=kernel_architecture,
            kernel_version=kernel_version,
            server=server,
            server_pid=server_pid,
            server_version=server_version,
            storage=storage,
            storage_version=storage_version,
        )

        environment.additional_properties = d
        return environment

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
