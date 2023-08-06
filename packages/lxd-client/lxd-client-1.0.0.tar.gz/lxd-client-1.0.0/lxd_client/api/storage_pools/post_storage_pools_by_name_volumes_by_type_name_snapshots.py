from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.background_operation_response import BackgroundOperationResponse
from ...models.create_storage_pools_by_name_volumes_by_type_name_snapshots_request import (
    CreateStoragePoolsByNameVolumesByTypeNameSnapshotsRequest,
)
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    pool: str,
    type: str,
    name: str,
    *,
    client: Client,
    json_body: CreateStoragePoolsByNameVolumesByTypeNameSnapshotsRequest,
) -> Dict[str, Any]:
    url = "{}/1.0/storage-pools/{pool}/volumes/{type}/{name}/snapshots".format(
        client.base_url, pool=pool, type=type, name=name
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
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
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[BackgroundOperationResponse, ErrorResponse]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    pool: str,
    type: str,
    name: str,
    *,
    client: Client,
    json_body: CreateStoragePoolsByNameVolumesByTypeNameSnapshotsRequest,
) -> Response[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Create a new volume snapshot

    Args:
        pool (str):
        type (str):
        name (str):
        json_body (CreateStoragePoolsByNameVolumesByTypeNameSnapshotsRequest):  Example: {'name':
            'my-snapshot'}.

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        pool=pool,
        type=type,
        name=name,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    pool: str,
    type: str,
    name: str,
    *,
    client: Client,
    json_body: CreateStoragePoolsByNameVolumesByTypeNameSnapshotsRequest,
) -> Optional[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Create a new volume snapshot

    Args:
        pool (str):
        type (str):
        name (str):
        json_body (CreateStoragePoolsByNameVolumesByTypeNameSnapshotsRequest):  Example: {'name':
            'my-snapshot'}.

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    return sync_detailed(
        pool=pool,
        type=type,
        name=name,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    pool: str,
    type: str,
    name: str,
    *,
    client: Client,
    json_body: CreateStoragePoolsByNameVolumesByTypeNameSnapshotsRequest,
) -> Response[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Create a new volume snapshot

    Args:
        pool (str):
        type (str):
        name (str):
        json_body (CreateStoragePoolsByNameVolumesByTypeNameSnapshotsRequest):  Example: {'name':
            'my-snapshot'}.

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        pool=pool,
        type=type,
        name=name,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    pool: str,
    type: str,
    name: str,
    *,
    client: Client,
    json_body: CreateStoragePoolsByNameVolumesByTypeNameSnapshotsRequest,
) -> Optional[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Create a new volume snapshot

    Args:
        pool (str):
        type (str):
        name (str):
        json_body (CreateStoragePoolsByNameVolumesByTypeNameSnapshotsRequest):  Example: {'name':
            'my-snapshot'}.

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    return (
        await asyncio_detailed(
            pool=pool,
            type=type,
            name=name,
            client=client,
            json_body=json_body,
        )
    ).parsed
