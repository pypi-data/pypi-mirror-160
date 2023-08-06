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
    secret: str,
) -> Dict[str, Any]:
    url = "{}/1.0/operations/{uuid}/websocket".format(client.base_url, uuid=uuid)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["recursion"] = recursion

    params["filter"] = filter_

    params["secret"] = secret

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
    secret: str,
) -> Response[Union[BackgroundOperationResponse, ErrorResponse]]:
    """-< This connection is upgraded into a websocket connection speaking the protocol defined by the
    operation type. For example, in the case of an exec operation, the websocket is the bidirectional
    pipe for stdin/stdout/stderr to flow to and from the process inside the instance. In the case of
    migration, it will be the primary interface over which the migration information is communicated.
    The secret here is the one that was provided when the operation was created. Guests are allowed to
    connect provided they have the right secret.

    Args:
        uuid (str):
        recursion (Union[Unset, None, int]):
        filter_ (Union[Unset, None, str]):
        secret (str):  Example: SECRET.

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        client=client,
        recursion=recursion,
        filter_=filter_,
        secret=secret,
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
    secret: str,
) -> Optional[Union[BackgroundOperationResponse, ErrorResponse]]:
    """-< This connection is upgraded into a websocket connection speaking the protocol defined by the
    operation type. For example, in the case of an exec operation, the websocket is the bidirectional
    pipe for stdin/stdout/stderr to flow to and from the process inside the instance. In the case of
    migration, it will be the primary interface over which the migration information is communicated.
    The secret here is the one that was provided when the operation was created. Guests are allowed to
    connect provided they have the right secret.

    Args:
        uuid (str):
        recursion (Union[Unset, None, int]):
        filter_ (Union[Unset, None, str]):
        secret (str):  Example: SECRET.

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        recursion=recursion,
        filter_=filter_,
        secret=secret,
    ).parsed


async def asyncio_detailed(
    uuid: str,
    *,
    client: Client,
    recursion: Union[Unset, None, int] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
    secret: str,
) -> Response[Union[BackgroundOperationResponse, ErrorResponse]]:
    """-< This connection is upgraded into a websocket connection speaking the protocol defined by the
    operation type. For example, in the case of an exec operation, the websocket is the bidirectional
    pipe for stdin/stdout/stderr to flow to and from the process inside the instance. In the case of
    migration, it will be the primary interface over which the migration information is communicated.
    The secret here is the one that was provided when the operation was created. Guests are allowed to
    connect provided they have the right secret.

    Args:
        uuid (str):
        recursion (Union[Unset, None, int]):
        filter_ (Union[Unset, None, str]):
        secret (str):  Example: SECRET.

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        client=client,
        recursion=recursion,
        filter_=filter_,
        secret=secret,
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
    secret: str,
) -> Optional[Union[BackgroundOperationResponse, ErrorResponse]]:
    """-< This connection is upgraded into a websocket connection speaking the protocol defined by the
    operation type. For example, in the case of an exec operation, the websocket is the bidirectional
    pipe for stdin/stdout/stderr to flow to and from the process inside the instance. In the case of
    migration, it will be the primary interface over which the migration information is communicated.
    The secret here is the one that was provided when the operation was created. Guests are allowed to
    connect provided they have the right secret.

    Args:
        uuid (str):
        recursion (Union[Unset, None, int]):
        filter_ (Union[Unset, None, str]):
        secret (str):  Example: SECRET.

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            recursion=recursion,
            filter_=filter_,
            secret=secret,
        )
    ).parsed
