from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Metadata3")


@attr.s(auto_attribs=True)
class Metadata3:
    """
    Example:
        {'secret': '52e9ec5885562aa24d05d7b4846ebb8b5f1f7bf5cd6e285639b569d9eaf54c9b'}

    Attributes:
        secret (Union[Unset, str]):  Example: 52e9ec5885562aa24d05d7b4846ebb8b5f1f7bf5cd6e285639b569d9eaf54c9b.
    """

    secret: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        secret = self.secret

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if secret is not UNSET:
            field_dict["secret"] = secret

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        secret = d.pop("secret", UNSET)

        metadata_3 = cls(
            secret=secret,
        )

        metadata_3.additional_properties = d
        return metadata_3

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
