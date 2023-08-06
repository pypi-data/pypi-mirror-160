from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Secrets")


@attr.s(auto_attribs=True)
class Secrets:
    """
    Example:
        {'criu': 'my-other-secret', 'control': 'my-secret-string', 'fs': 'my third secret'}

    Attributes:
        control (Union[Unset, str]):  Example: my-secret-string.
        criu (Union[Unset, str]):  Example: my-other-secret.
        fs (Union[Unset, str]):  Example: my third secret.
    """

    control: Union[Unset, str] = UNSET
    criu: Union[Unset, str] = UNSET
    fs: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        control = self.control
        criu = self.criu
        fs = self.fs

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if control is not UNSET:
            field_dict["control"] = control
        if criu is not UNSET:
            field_dict["criu"] = criu
        if fs is not UNSET:
            field_dict["fs"] = fs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        control = d.pop("control", UNSET)

        criu = d.pop("criu", UNSET)

        fs = d.pop("fs", UNSET)

        secrets = cls(
            control=control,
            criu=criu,
            fs=fs,
        )

        secrets.additional_properties = d
        return secrets

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
