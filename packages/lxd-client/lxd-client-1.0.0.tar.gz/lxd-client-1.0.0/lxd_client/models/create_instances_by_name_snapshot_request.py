from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateInstancesByNameSnapshotRequest")


@attr.s(auto_attribs=True)
class CreateInstancesByNameSnapshotRequest:
    """
    Example:
        {'name': 'my-snapshot', 'stateful': True}

    Attributes:
        name (Union[Unset, str]): Name of the snapshot Example: my-snapshot.
        stateful (Union[Unset, bool]): Whether to include state too Example: True.
    """

    name: Union[Unset, str] = UNSET
    stateful: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        stateful = self.stateful

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if stateful is not UNSET:
            field_dict["stateful"] = stateful

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        stateful = d.pop("stateful", UNSET)

        create_instances_by_name_snapshot_request = cls(
            name=name,
            stateful=stateful,
        )

        create_instances_by_name_snapshot_request.additional_properties = d
        return create_instances_by_name_snapshot_request

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
