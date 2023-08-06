from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.metadata import Metadata
from ..models.resources import Resources
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetNetworksUUIDResponse")


@attr.s(auto_attribs=True)
class GetNetworksUUIDResponse:
    """
    Example:
        {'metadata': {'secret': 'c9209bee6df99315be1660dd215acde4aec89b8e5336039712fc11008d918b0d'}, 'status_code': 103,
            'updated_at': '2016-02-17T21:59:27.237Z', 'err': 'err', 'created_at': '2016-02-17T21:59:27.237Z', 'resources':
            {'images': ['/1.0/images/54c8caac1f61901ed86c68f24af5f5d3672bdc62c71d04f06df3a59e95684473']}, 'id':
            'b8d84888-1dc2-44fd-b386-7f679e171ba5', 'class': 'token', 'status': 'Running', 'may_cancel': True}

    Attributes:
        id (Union[Unset, str]):  Example: b8d84888-1dc2-44fd-b386-7f679e171ba5.
        class_ (Union[Unset, str]):  Example: token.
        created_at (Union[Unset, str]):  Example: 2016-02-17T21:59:27.237Z.
        updated_at (Union[Unset, str]):  Example: 2016-02-17T21:59:27.237Z.
        status (Union[Unset, str]):  Example: Running.
        status_code (Union[Unset, float]):  Example: 103.
        resources (Union[Unset, Resources]):  Example: {'images':
            ['/1.0/images/54c8caac1f61901ed86c68f24af5f5d3672bdc62c71d04f06df3a59e95684473']}.
        metadata (Union[Unset, Metadata]):  Example: {'secret':
            'c9209bee6df99315be1660dd215acde4aec89b8e5336039712fc11008d918b0d'}.
        may_cancel (Union[Unset, bool]):  Example: True.
        err (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    class_: Union[Unset, str] = UNSET
    created_at: Union[Unset, str] = UNSET
    updated_at: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    status_code: Union[Unset, float] = UNSET
    resources: Union[Unset, Resources] = UNSET
    metadata: Union[Unset, Metadata] = UNSET
    may_cancel: Union[Unset, bool] = UNSET
    err: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        class_ = self.class_
        created_at = self.created_at
        updated_at = self.updated_at
        status = self.status
        status_code = self.status_code
        resources: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.resources, Unset):
            resources = self.resources.to_dict()

        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        may_cancel = self.may_cancel
        err = self.err

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if class_ is not UNSET:
            field_dict["class"] = class_
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if status is not UNSET:
            field_dict["status"] = status
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if resources is not UNSET:
            field_dict["resources"] = resources
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if may_cancel is not UNSET:
            field_dict["may_cancel"] = may_cancel
        if err is not UNSET:
            field_dict["err"] = err

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        class_ = d.pop("class", UNSET)

        created_at = d.pop("created_at", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        status = d.pop("status", UNSET)

        status_code = d.pop("status_code", UNSET)

        _resources = d.pop("resources", UNSET)
        resources: Union[Unset, Resources]
        if isinstance(_resources, Unset):
            resources = UNSET
        else:
            resources = Resources.from_dict(_resources)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, Metadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata.from_dict(_metadata)

        may_cancel = d.pop("may_cancel", UNSET)

        err = d.pop("err", UNSET)

        get_networks_uuid_response = cls(
            id=id,
            class_=class_,
            created_at=created_at,
            updated_at=updated_at,
            status=status,
            status_code=status_code,
            resources=resources,
            metadata=metadata,
            may_cancel=may_cancel,
            err=err,
        )

        get_networks_uuid_response.additional_properties = d
        return get_networks_uuid_response

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
