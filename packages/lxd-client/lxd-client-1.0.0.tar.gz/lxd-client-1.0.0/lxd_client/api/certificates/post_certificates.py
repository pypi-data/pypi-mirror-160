from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.background_operation_response import BackgroundOperationResponse
from ...models.create_certificates_request import CreateCertificatesRequest
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: CreateCertificatesRequest,
) -> Dict[str, Any]:
    url = "{}/1.0/certificates".format(client.base_url)

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
    *,
    client: Client,
    json_body: CreateCertificatesRequest,
) -> Response[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Add a new trusted certificate

    Args:
        json_body (CreateCertificatesRequest):  Example: {'password': 'server-trust-password',
            'certificate': 'PEM certificate', 'name': 'foo', 'type': 'client'}.

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: CreateCertificatesRequest,
) -> Optional[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Add a new trusted certificate

    Args:
        json_body (CreateCertificatesRequest):  Example: {'password': 'server-trust-password',
            'certificate': 'PEM certificate', 'name': 'foo', 'type': 'client'}.

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: CreateCertificatesRequest,
) -> Response[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Add a new trusted certificate

    Args:
        json_body (CreateCertificatesRequest):  Example: {'password': 'server-trust-password',
            'certificate': 'PEM certificate', 'name': 'foo', 'type': 'client'}.

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: CreateCertificatesRequest,
) -> Optional[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Add a new trusted certificate

    Args:
        json_body (CreateCertificatesRequest):  Example: {'password': 'server-trust-password',
            'certificate': 'PEM certificate', 'name': 'foo', 'type': 'client'}.

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
