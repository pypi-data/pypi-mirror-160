from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.open_trade_schema import OpenTradeSchema
from ...types import Response


def _get_kwargs(
    tradeid: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/v1/trade/{tradeid}".format(client.base_url, tradeid=tradeid)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[HTTPValidationError, OpenTradeSchema]]:
    if response.status_code == 200:
        response_200 = OpenTradeSchema.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[HTTPValidationError, OpenTradeSchema]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    tradeid: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, OpenTradeSchema]]:
    """Trade

    Args:
        tradeid (int):

    Returns:
        Response[Union[HTTPValidationError, OpenTradeSchema]]
    """

    kwargs = _get_kwargs(
        tradeid=tradeid,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    tradeid: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, OpenTradeSchema]]:
    """Trade

    Args:
        tradeid (int):

    Returns:
        Response[Union[HTTPValidationError, OpenTradeSchema]]
    """

    return sync_detailed(
        tradeid=tradeid,
        client=client,
    ).parsed


async def asyncio_detailed(
    tradeid: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, OpenTradeSchema]]:
    """Trade

    Args:
        tradeid (int):

    Returns:
        Response[Union[HTTPValidationError, OpenTradeSchema]]
    """

    kwargs = _get_kwargs(
        tradeid=tradeid,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    tradeid: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, OpenTradeSchema]]:
    """Trade

    Args:
        tradeid (int):

    Returns:
        Response[Union[HTTPValidationError, OpenTradeSchema]]
    """

    return (
        await asyncio_detailed(
            tradeid=tradeid,
            client=client,
        )
    ).parsed
