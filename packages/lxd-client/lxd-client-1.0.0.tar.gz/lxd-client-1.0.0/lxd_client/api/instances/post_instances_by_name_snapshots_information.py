from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.background_operation_response import BackgroundOperationResponse
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    name: str,
    snapshot_name: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/1.0/instances/{name}/snapshots/{snapshotName}".format(
        client.base_url, name=name, snapshotName=snapshot_name
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[BackgroundOperationResponse, ErrorResponse]]:
    if response.status_code == 202:
        response_202 = BackgroundOperationResponse.from_dict(response.json())

        return response_202
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401
    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409
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
    snapshot_name: str,
    *,
    client: Client,
) -> Response[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Used to rename/migrate the snapshot

    Args:
        name (str):
        snapshot_name (str):

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        name=name,
        snapshot_name=snapshot_name,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    name: str,
    snapshot_name: str,
    *,
    client: Client,
) -> Optional[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Used to rename/migrate the snapshot

    Args:
        name (str):
        snapshot_name (str):

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    return sync_detailed(
        name=name,
        snapshot_name=snapshot_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    name: str,
    snapshot_name: str,
    *,
    client: Client,
) -> Response[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Used to rename/migrate the snapshot

    Args:
        name (str):
        snapshot_name (str):

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        name=name,
        snapshot_name=snapshot_name,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    name: str,
    snapshot_name: str,
    *,
    client: Client,
) -> Optional[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Used to rename/migrate the snapshot

    Args:
        name (str):
        snapshot_name (str):

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    return (
        await asyncio_detailed(
            name=name,
            snapshot_name=snapshot_name,
            client=client,
        )
    ).parsed
