from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.locks import Locks
from ...types import Response


def _get_kwargs(
    lockid: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/v1/locks/{lockid}".format(client.base_url, lockid=lockid)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[HTTPValidationError, Locks]]:
    if response.status_code == 200:
        response_200 = Locks.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[HTTPValidationError, Locks]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    lockid: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, Locks]]:
    """Delete Lock

    Args:
        lockid (int):

    Returns:
        Response[Union[HTTPValidationError, Locks]]
    """

    kwargs = _get_kwargs(
        lockid=lockid,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    lockid: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, Locks]]:
    """Delete Lock

    Args:
        lockid (int):

    Returns:
        Response[Union[HTTPValidationError, Locks]]
    """

    return sync_detailed(
        lockid=lockid,
        client=client,
    ).parsed


async def asyncio_detailed(
    lockid: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, Locks]]:
    """Delete Lock

    Args:
        lockid (int):

    Returns:
        Response[Union[HTTPValidationError, Locks]]
    """

    kwargs = _get_kwargs(
        lockid=lockid,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    lockid: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, Locks]]:
    """Delete Lock

    Args:
        lockid (int):

    Returns:
        Response[Union[HTTPValidationError, Locks]]
    """

    return (
        await asyncio_detailed(
            lockid=lockid,
            client=client,
        )
    ).parsed
