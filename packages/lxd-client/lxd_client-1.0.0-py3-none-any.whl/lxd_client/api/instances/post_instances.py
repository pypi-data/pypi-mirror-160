from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.background_operation_response import BackgroundOperationResponse
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    target: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/1.0/instances".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["target"] = target

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
    *,
    client: Client,
    target: Union[Unset, None, str] = UNSET,
) -> Response[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Create a new instance

    Args:
        target (Union[Unset, None, str]):

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        target=target,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    target: Union[Unset, None, str] = UNSET,
) -> Optional[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Create a new instance

    Args:
        target (Union[Unset, None, str]):

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    return sync_detailed(
        client=client,
        target=target,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    target: Union[Unset, None, str] = UNSET,
) -> Response[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Create a new instance

    Args:
        target (Union[Unset, None, str]):

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        target=target,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    target: Union[Unset, None, str] = UNSET,
) -> Optional[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Create a new instance

    Args:
        target (Union[Unset, None, str]):

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    return (
        await asyncio_detailed(
            client=client,
            target=target,
        )
    ).parsed
