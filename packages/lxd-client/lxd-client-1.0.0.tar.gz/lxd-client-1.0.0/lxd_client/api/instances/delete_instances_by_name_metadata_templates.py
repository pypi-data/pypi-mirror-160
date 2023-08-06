from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.background_operation_response import BackgroundOperationResponse
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response


def _get_kwargs(
    name: str,
    *,
    client: Client,
    path: str,
) -> Dict[str, Any]:
    url = "{}/1.0/instances/{name}/metadata/templates".format(client.base_url, name=name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["path"] = path

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "delete",
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
    path: str,
) -> Response[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Delete an instance template

    Args:
        name (str):
        path (str):

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        name=name,
        client=client,
        path=path,
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
    path: str,
) -> Optional[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Delete an instance template

    Args:
        name (str):
        path (str):

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    return sync_detailed(
        name=name,
        client=client,
        path=path,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: Client,
    path: str,
) -> Response[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Delete an instance template

    Args:
        name (str):
        path (str):

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        name=name,
        client=client,
        path=path,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    name: str,
    *,
    client: Client,
    path: str,
) -> Optional[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Delete an instance template

    Args:
        name (str):
        path (str):

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            path=path,
        )
    ).parsed
