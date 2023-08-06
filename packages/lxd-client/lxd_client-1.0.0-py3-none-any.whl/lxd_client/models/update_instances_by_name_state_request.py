from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateInstancesByNameStateRequest")


@attr.s(auto_attribs=True)
class UpdateInstancesByNameStateRequest:
    """
    Example:
        {'action': 'stop', 'force': True, 'timeout': 30, 'stateful': True}

    Attributes:
        action (Union[Unset, str]): State change action (stop, start, restart, freeze or unfreeze) Example: stop.
        timeout (Union[Unset, float]): A timeout after which the state change is considered as failed Example: 30.
        force (Union[Unset, bool]): Force the state change (currently only valid for stop and restart where it means
            killing the instance) Example: True.
        stateful (Union[Unset, bool]): Whether to store or restore runtime state before stopping or startiong (only
            valid for stop and start, defaults to false) Example: True.
    """

    action: Union[Unset, str] = UNSET
    timeout: Union[Unset, float] = UNSET
    force: Union[Unset, bool] = UNSET
    stateful: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        action = self.action
        timeout = self.timeout
        force = self.force
        stateful = self.stateful

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if action is not UNSET:
            field_dict["action"] = action
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if force is not UNSET:
            field_dict["force"] = force
        if stateful is not UNSET:
            field_dict["stateful"] = stateful

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        action = d.pop("action", UNSET)

        timeout = d.pop("timeout", UNSET)

        force = d.pop("force", UNSET)

        stateful = d.pop("stateful", UNSET)

        update_instances_by_name_state_request = cls(
            action=action,
            timeout=timeout,
            force=force,
            stateful=stateful,
        )

        update_instances_by_name_state_request.additional_properties = d
        return update_instances_by_name_state_request

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
