from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.background_operation_response import BackgroundOperationResponse
from ...models.error_response import ErrorResponse
from ...models.update_networks_by_name_request import UpdateNetworksByNameRequest
from ...types import Response


def _get_kwargs(
    name: str,
    *,
    client: Client,
    json_body: UpdateNetworksByNameRequest,
) -> Dict[str, Any]:
    url = "{}/1.0/networks/{name}".format(client.base_url, name=name)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
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
    json_body: UpdateNetworksByNameRequest,
) -> Response[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Replace the network information

    Args:
        name (str):
        json_body (UpdateNetworksByNameRequest):  Example: {'bridge.driver': 'openvswitch',
            'ipv4.address': '10.0.3.1/24', 'ipv6.address': 'fd1:6997:4939:495d::1/64'}.

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
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
    name: str,
    *,
    client: Client,
    json_body: UpdateNetworksByNameRequest,
) -> Optional[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Replace the network information

    Args:
        name (str):
        json_body (UpdateNetworksByNameRequest):  Example: {'bridge.driver': 'openvswitch',
            'ipv4.address': '10.0.3.1/24', 'ipv6.address': 'fd1:6997:4939:495d::1/64'}.

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    return sync_detailed(
        name=name,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: Client,
    json_body: UpdateNetworksByNameRequest,
) -> Response[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Replace the network information

    Args:
        name (str):
        json_body (UpdateNetworksByNameRequest):  Example: {'bridge.driver': 'openvswitch',
            'ipv4.address': '10.0.3.1/24', 'ipv6.address': 'fd1:6997:4939:495d::1/64'}.

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        name=name,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    name: str,
    *,
    client: Client,
    json_body: UpdateNetworksByNameRequest,
) -> Optional[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Replace the network information

    Args:
        name (str):
        json_body (UpdateNetworksByNameRequest):  Example: {'bridge.driver': 'openvswitch',
            'ipv4.address': '10.0.3.1/24', 'ipv6.address': 'fd1:6997:4939:495d::1/64'}.

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            json_body=json_body,
        )
    ).parsed
