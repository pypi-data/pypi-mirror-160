from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetOperationsResponse")


@attr.s(auto_attribs=True)
class GetOperationsResponse:
    """
    Example:
        {'running': ['/1.0/operations/092a8755-fd90-4ce4-bf91-9f87d03fd5bc'], 'success':
            ['/1.0/operations/c0fc0d0d-a997-462b-842b-f8bd0df82507']}

    Attributes:
        success (Union[Unset, List[str]]):  Example: ['/1.0/operations/c0fc0d0d-a997-462b-842b-f8bd0df82507'].
        running (Union[Unset, List[str]]):  Example: ['/1.0/operations/092a8755-fd90-4ce4-bf91-9f87d03fd5bc'].
    """

    success: Union[Unset, List[str]] = UNSET
    running: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        success: Union[Unset, List[str]] = UNSET
        if not isinstance(self.success, Unset):
            success = self.success

        running: Union[Unset, List[str]] = UNSET
        if not isinstance(self.running, Unset):
            running = self.running

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if success is not UNSET:
            field_dict["success"] = success
        if running is not UNSET:
            field_dict["running"] = running

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        success = cast(List[str], d.pop("success", UNSET))

        running = cast(List[str], d.pop("running", UNSET))

        get_operations_response = cls(
            success=success,
            running=running,
        )

        get_operations_response.additional_properties = d
        return get_operations_response

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
