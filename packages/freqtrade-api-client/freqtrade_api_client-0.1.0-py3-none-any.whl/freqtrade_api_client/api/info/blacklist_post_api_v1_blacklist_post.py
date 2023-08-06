from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.blacklist_payload import BlacklistPayload
from ...models.blacklist_response import BlacklistResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: BlacklistPayload,
) -> Dict[str, Any]:
    url = "{}/api/v1/blacklist".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[BlacklistResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = BlacklistResponse.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[BlacklistResponse, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: BlacklistPayload,
) -> Response[Union[BlacklistResponse, HTTPValidationError]]:
    """Blacklist Post

    Args:
        json_body (BlacklistPayload):

    Returns:
        Response[Union[BlacklistResponse, HTTPValidationError]]
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
    client: AuthenticatedClient,
    json_body: BlacklistPayload,
) -> Optional[Union[BlacklistResponse, HTTPValidationError]]:
    """Blacklist Post

    Args:
        json_body (BlacklistPayload):

    Returns:
        Response[Union[BlacklistResponse, HTTPValidationError]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: BlacklistPayload,
) -> Response[Union[BlacklistResponse, HTTPValidationError]]:
    """Blacklist Post

    Args:
        json_body (BlacklistPayload):

    Returns:
        Response[Union[BlacklistResponse, HTTPValidationError]]
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
    client: AuthenticatedClient,
    json_body: BlacklistPayload,
) -> Optional[Union[BlacklistResponse, HTTPValidationError]]:
    """Blacklist Post

    Args:
        json_body (BlacklistPayload):

    Returns:
        Response[Union[BlacklistResponse, HTTPValidationError]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
