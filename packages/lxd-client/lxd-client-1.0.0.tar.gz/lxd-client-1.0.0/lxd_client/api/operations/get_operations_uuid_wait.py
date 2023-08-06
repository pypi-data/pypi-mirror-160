from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.background_operation_response import BackgroundOperationResponse
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    uuid: str,
    *,
    client: Client,
    recursion: Union[Unset, None, int] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
    timeout: Union[Unset, None, float] = UNSET,
) -> Dict[str, Any]:
    url = "{}/1.0/operations/{uuid}/wait".format(client.base_url, uuid=uuid)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["recursion"] = recursion

    params["filter"] = filter_

    params["timeout"] = timeout

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
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
    uuid: str,
    *,
    client: Client,
    recursion: Union[Unset, None, int] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
    timeout: Union[Unset, None, float] = UNSET,
) -> Response[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Wait for an operation to finish

    Args:
        uuid (str):
        recursion (Union[Unset, None, int]):
        filter_ (Union[Unset, None, str]):
        timeout (Union[Unset, None, float]):  Example: 30.

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        client=client,
        recursion=recursion,
        filter_=filter_,
        timeout=timeout,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    uuid: str,
    *,
    client: Client,
    recursion: Union[Unset, None, int] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
    timeout: Union[Unset, None, float] = UNSET,
) -> Optional[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Wait for an operation to finish

    Args:
        uuid (str):
        recursion (Union[Unset, None, int]):
        filter_ (Union[Unset, None, str]):
        timeout (Union[Unset, None, float]):  Example: 30.

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        recursion=recursion,
        filter_=filter_,
        timeout=timeout,
    ).parsed


async def asyncio_detailed(
    uuid: str,
    *,
    client: Client,
    recursion: Union[Unset, None, int] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
    timeout: Union[Unset, None, float] = UNSET,
) -> Response[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Wait for an operation to finish

    Args:
        uuid (str):
        recursion (Union[Unset, None, int]):
        filter_ (Union[Unset, None, str]):
        timeout (Union[Unset, None, float]):  Example: 30.

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        client=client,
        recursion=recursion,
        filter_=filter_,
        timeout=timeout,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    uuid: str,
    *,
    client: Client,
    recursion: Union[Unset, None, int] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
    timeout: Union[Unset, None, float] = UNSET,
) -> Optional[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Wait for an operation to finish

    Args:
        uuid (str):
        recursion (Union[Unset, None, int]):
        filter_ (Union[Unset, None, str]):
        timeout (Union[Unset, None, float]):  Example: 30.

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            recursion=recursion,
            filter_=filter_,
            timeout=timeout,
        )
    ).parsed
