from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.background_operation_response import BackgroundOperationResponse
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    name: str,
    *,
    client: Client,
    path: Union[Unset, None, str] = UNSET,
    x_lxd_uid: Union[Unset, int] = UNSET,
    x_lxd_gid: Union[Unset, int] = UNSET,
    x_lxd_mode: Union[Unset, int] = UNSET,
    x_lxd_write: Union[Unset, str] = UNSET,
    x_lxd_type: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/1.0/instances/{name}/files".format(client.base_url, name=name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(x_lxd_uid, Unset):
        headers["X-LXD-uid"] = str(x_lxd_uid)

    if not isinstance(x_lxd_gid, Unset):
        headers["X-LXD-gid"] = str(x_lxd_gid)

    if not isinstance(x_lxd_mode, Unset):
        headers["X-LXD-mode"] = str(x_lxd_mode)

    if not isinstance(x_lxd_write, Unset):
        headers["X-LXD-write"] = x_lxd_write

    if not isinstance(x_lxd_type, Unset):
        headers["X-LXD-type"] = x_lxd_type

    params: Dict[str, Any] = {}
    params["path"] = path

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[BackgroundOperationResponse, ErrorResponse]]:
    if response.status_code == 200:
        response_200 = BackgroundOperationResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[BackgroundOperationResponse, ErrorResponse]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    name: str,
    *,
    client: Client,
    path: Union[Unset, None, str] = UNSET,
    x_lxd_uid: Union[Unset, int] = UNSET,
    x_lxd_gid: Union[Unset, int] = UNSET,
    x_lxd_mode: Union[Unset, int] = UNSET,
    x_lxd_write: Union[Unset, str] = UNSET,
    x_lxd_type: Union[Unset, str] = UNSET,
) -> Response[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Upload a file to the instance

    Args:
        name (str):
        path (Union[Unset, None, str]):
        x_lxd_uid (Union[Unset, int]):
        x_lxd_gid (Union[Unset, int]):
        x_lxd_mode (Union[Unset, int]):
        x_lxd_write (Union[Unset, str]):
        x_lxd_type (Union[Unset, str]):

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        name=name,
        client=client,
        path=path,
        x_lxd_uid=x_lxd_uid,
        x_lxd_gid=x_lxd_gid,
        x_lxd_mode=x_lxd_mode,
        x_lxd_write=x_lxd_write,
        x_lxd_type=x_lxd_type,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    name: str,
    *,
    client: Client,
    path: Union[Unset, None, str] = UNSET,
    x_lxd_uid: Union[Unset, int] = UNSET,
    x_lxd_gid: Union[Unset, int] = UNSET,
    x_lxd_mode: Union[Unset, int] = UNSET,
    x_lxd_write: Union[Unset, str] = UNSET,
    x_lxd_type: Union[Unset, str] = UNSET,
) -> Optional[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Upload a file to the instance

    Args:
        name (str):
        path (Union[Unset, None, str]):
        x_lxd_uid (Union[Unset, int]):
        x_lxd_gid (Union[Unset, int]):
        x_lxd_mode (Union[Unset, int]):
        x_lxd_write (Union[Unset, str]):
        x_lxd_type (Union[Unset, str]):

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    return sync_detailed(
        name=name,
        client=client,
        path=path,
        x_lxd_uid=x_lxd_uid,
        x_lxd_gid=x_lxd_gid,
        x_lxd_mode=x_lxd_mode,
        x_lxd_write=x_lxd_write,
        x_lxd_type=x_lxd_type,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: Client,
    path: Union[Unset, None, str] = UNSET,
    x_lxd_uid: Union[Unset, int] = UNSET,
    x_lxd_gid: Union[Unset, int] = UNSET,
    x_lxd_mode: Union[Unset, int] = UNSET,
    x_lxd_write: Union[Unset, str] = UNSET,
    x_lxd_type: Union[Unset, str] = UNSET,
) -> Response[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Upload a file to the instance

    Args:
        name (str):
        path (Union[Unset, None, str]):
        x_lxd_uid (Union[Unset, int]):
        x_lxd_gid (Union[Unset, int]):
        x_lxd_mode (Union[Unset, int]):
        x_lxd_write (Union[Unset, str]):
        x_lxd_type (Union[Unset, str]):

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        name=name,
        client=client,
        path=path,
        x_lxd_uid=x_lxd_uid,
        x_lxd_gid=x_lxd_gid,
        x_lxd_mode=x_lxd_mode,
        x_lxd_write=x_lxd_write,
        x_lxd_type=x_lxd_type,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    name: str,
    *,
    client: Client,
    path: Union[Unset, None, str] = UNSET,
    x_lxd_uid: Union[Unset, int] = UNSET,
    x_lxd_gid: Union[Unset, int] = UNSET,
    x_lxd_mode: Union[Unset, int] = UNSET,
    x_lxd_write: Union[Unset, str] = UNSET,
    x_lxd_type: Union[Unset, str] = UNSET,
) -> Optional[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Upload a file to the instance

    Args:
        name (str):
        path (Union[Unset, None, str]):
        x_lxd_uid (Union[Unset, int]):
        x_lxd_gid (Union[Unset, int]):
        x_lxd_mode (Union[Unset, int]):
        x_lxd_write (Union[Unset, str]):
        x_lxd_type (Union[Unset, str]):

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            path=path,
            x_lxd_uid=x_lxd_uid,
            x_lxd_gid=x_lxd_gid,
            x_lxd_mode=x_lxd_mode,
            x_lxd_write=x_lxd_write,
            x_lxd_type=x_lxd_type,
        )
    ).parsed
