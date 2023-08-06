from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.strategy_response import StrategyResponse
from ...types import Response


def _get_kwargs(
    strategy: str,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/v1/strategy/{strategy}".format(client.base_url, strategy=strategy)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[HTTPValidationError, StrategyResponse]]:
    if response.status_code == 200:
        response_200 = StrategyResponse.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[HTTPValidationError, StrategyResponse]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    strategy: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, StrategyResponse]]:
    """Get Strategy

    Args:
        strategy (str):

    Returns:
        Response[Union[HTTPValidationError, StrategyResponse]]
    """

    kwargs = _get_kwargs(
        strategy=strategy,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    strategy: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, StrategyResponse]]:
    """Get Strategy

    Args:
        strategy (str):

    Returns:
        Response[Union[HTTPValidationError, StrategyResponse]]
    """

    return sync_detailed(
        strategy=strategy,
        client=client,
    ).parsed


async def asyncio_detailed(
    strategy: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, StrategyResponse]]:
    """Get Strategy

    Args:
        strategy (str):

    Returns:
        Response[Union[HTTPValidationError, StrategyResponse]]
    """

    kwargs = _get_kwargs(
        strategy=strategy,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    strategy: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, StrategyResponse]]:
    """Get Strategy

    Args:
        strategy (str):

    Returns:
        Response[Union[HTTPValidationError, StrategyResponse]]
    """

    return (
        await asyncio_detailed(
            strategy=strategy,
            client=client,
        )
    ).parsed
