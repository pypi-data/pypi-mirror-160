from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.daily import Daily
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    timescale: Union[Unset, None, int] = 7,
) -> Dict[str, Any]:
    url = "{}/api/v1/daily".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["timescale"] = timescale

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Daily, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = Daily.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Daily, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    timescale: Union[Unset, None, int] = 7,
) -> Response[Union[Daily, HTTPValidationError]]:
    """Daily

    Args:
        timescale (Union[Unset, None, int]):  Default: 7.

    Returns:
        Response[Union[Daily, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        timescale=timescale,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    timescale: Union[Unset, None, int] = 7,
) -> Optional[Union[Daily, HTTPValidationError]]:
    """Daily

    Args:
        timescale (Union[Unset, None, int]):  Default: 7.

    Returns:
        Response[Union[Daily, HTTPValidationError]]
    """

    return sync_detailed(
        client=client,
        timescale=timescale,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    timescale: Union[Unset, None, int] = 7,
) -> Response[Union[Daily, HTTPValidationError]]:
    """Daily

    Args:
        timescale (Union[Unset, None, int]):  Default: 7.

    Returns:
        Response[Union[Daily, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        timescale=timescale,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    timescale: Union[Unset, None, int] = 7,
) -> Optional[Union[Daily, HTTPValidationError]]:
    """Daily

    Args:
        timescale (Union[Unset, None, int]):  Default: 7.

    Returns:
        Response[Union[Daily, HTTPValidationError]]
    """

    return (
        await asyncio_detailed(
            client=client,
            timescale=timescale,
        )
    ).parsed
