from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.pair_history import PairHistory
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    pair: str,
    timeframe: str,
    limit: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/pair_candles".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["pair"] = pair

    params["timeframe"] = timeframe

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[HTTPValidationError, PairHistory]]:
    if response.status_code == 200:
        response_200 = PairHistory.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[HTTPValidationError, PairHistory]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    pair: str,
    timeframe: str,
    limit: Union[Unset, None, int] = UNSET,
) -> Response[Union[HTTPValidationError, PairHistory]]:
    """Pair Candles

    Args:
        pair (str):
        timeframe (str):
        limit (Union[Unset, None, int]):

    Returns:
        Response[Union[HTTPValidationError, PairHistory]]
    """

    kwargs = _get_kwargs(
        client=client,
        pair=pair,
        timeframe=timeframe,
        limit=limit,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    pair: str,
    timeframe: str,
    limit: Union[Unset, None, int] = UNSET,
) -> Optional[Union[HTTPValidationError, PairHistory]]:
    """Pair Candles

    Args:
        pair (str):
        timeframe (str):
        limit (Union[Unset, None, int]):

    Returns:
        Response[Union[HTTPValidationError, PairHistory]]
    """

    return sync_detailed(
        client=client,
        pair=pair,
        timeframe=timeframe,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    pair: str,
    timeframe: str,
    limit: Union[Unset, None, int] = UNSET,
) -> Response[Union[HTTPValidationError, PairHistory]]:
    """Pair Candles

    Args:
        pair (str):
        timeframe (str):
        limit (Union[Unset, None, int]):

    Returns:
        Response[Union[HTTPValidationError, PairHistory]]
    """

    kwargs = _get_kwargs(
        client=client,
        pair=pair,
        timeframe=timeframe,
        limit=limit,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    pair: str,
    timeframe: str,
    limit: Union[Unset, None, int] = UNSET,
) -> Optional[Union[HTTPValidationError, PairHistory]]:
    """Pair Candles

    Args:
        pair (str):
        timeframe (str):
        limit (Union[Unset, None, int]):

    Returns:
        Response[Union[HTTPValidationError, PairHistory]]
    """

    return (
        await asyncio_detailed(
            client=client,
            pair=pair,
            timeframe=timeframe,
            limit=limit,
        )
    ).parsed
