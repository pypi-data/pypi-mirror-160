from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.background_operation_response import BackgroundOperationResponse
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    pool: str,
    type: str,
    name: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/1.0/storage-pools/{pool}/volumes/{type}/{name}".format(client.base_url, pool=pool, type=type, name=name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
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
    pool: str,
    type: str,
    name: str,
    *,
    client: Client,
) -> Response[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Replace the storage volume information or restore from snapshot

    Args:
        pool (str):
        type (str):
        name (str):

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        pool=pool,
        type=type,
        name=name,
        client=client,
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
) -> Optional[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Replace the storage volume information or restore from snapshot

    Args:
        pool (str):
        type (str):
        name (str):

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    return sync_detailed(
        pool=pool,
        type=type,
        name=name,
        client=client,
    ).parsed


async def asyncio_detailed(
    pool: str,
    type: str,
    name: str,
    *,
    client: Client,
) -> Response[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Replace the storage volume information or restore from snapshot

    Args:
        pool (str):
        type (str):
        name (str):

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        pool=pool,
        type=type,
        name=name,
        client=client,
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
) -> Optional[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Replace the storage volume information or restore from snapshot

    Args:
        pool (str):
        type (str):
        name (str):

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    return (
        await asyncio_detailed(
            pool=pool,
            type=type,
            name=name,
            client=client,
        )
    ).parsed
