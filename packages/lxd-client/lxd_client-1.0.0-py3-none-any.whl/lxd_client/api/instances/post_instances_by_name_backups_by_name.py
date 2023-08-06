from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.background_operation_response import BackgroundOperationResponse
from ...models.create_instances_by_name_backups_by_name_request import CreateInstancesByNameBackupsByNameRequest
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    name: str,
    backups_name: str,
    *,
    client: Client,
    json_body: CreateInstancesByNameBackupsByNameRequest,
) -> Dict[str, Any]:
    url = "{}/1.0/instances/{name}/backups/{backupsName}".format(client.base_url, name=name, backupsName=backups_name)

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
    name: str,
    backups_name: str,
    *,
    client: Client,
    json_body: CreateInstancesByNameBackupsByNameRequest,
) -> Response[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Used to rename the backup

    Args:
        name (str):
        backups_name (str):
        json_body (CreateInstancesByNameBackupsByNameRequest):  Example: {'name': 'new-name'}.

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        name=name,
        backups_name=backups_name,
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
    backups_name: str,
    *,
    client: Client,
    json_body: CreateInstancesByNameBackupsByNameRequest,
) -> Optional[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Used to rename the backup

    Args:
        name (str):
        backups_name (str):
        json_body (CreateInstancesByNameBackupsByNameRequest):  Example: {'name': 'new-name'}.

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    return sync_detailed(
        name=name,
        backups_name=backups_name,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    name: str,
    backups_name: str,
    *,
    client: Client,
    json_body: CreateInstancesByNameBackupsByNameRequest,
) -> Response[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Used to rename the backup

    Args:
        name (str):
        backups_name (str):
        json_body (CreateInstancesByNameBackupsByNameRequest):  Example: {'name': 'new-name'}.

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        name=name,
        backups_name=backups_name,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    name: str,
    backups_name: str,
    *,
    client: Client,
    json_body: CreateInstancesByNameBackupsByNameRequest,
) -> Optional[Union[BackgroundOperationResponse, ErrorResponse]]:
    """Used to rename the backup

    Args:
        name (str):
        backups_name (str):
        json_body (CreateInstancesByNameBackupsByNameRequest):  Example: {'name': 'new-name'}.

    Returns:
        Response[Union[BackgroundOperationResponse, ErrorResponse]]
    """

    return (
        await asyncio_detailed(
            name=name,
            backups_name=backups_name,
            client=client,
            json_body=json_body,
        )
    ).parsed
