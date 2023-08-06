from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.backtest_response import BacktestResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    filename: str,
    strategy: str,
) -> Dict[str, Any]:
    url = "{}/api/v1/backtest/history/result".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["filename"] = filename

    params["strategy"] = strategy

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[BacktestResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = BacktestResponse.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[BacktestResponse, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    filename: str,
    strategy: str,
) -> Response[Union[BacktestResponse, HTTPValidationError]]:
    """Api Backtest History Result

    Args:
        filename (str):
        strategy (str):

    Returns:
        Response[Union[BacktestResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        filename=filename,
        strategy=strategy,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    filename: str,
    strategy: str,
) -> Optional[Union[BacktestResponse, HTTPValidationError]]:
    """Api Backtest History Result

    Args:
        filename (str):
        strategy (str):

    Returns:
        Response[Union[BacktestResponse, HTTPValidationError]]
    """

    return sync_detailed(
        client=client,
        filename=filename,
        strategy=strategy,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    filename: str,
    strategy: str,
) -> Response[Union[BacktestResponse, HTTPValidationError]]:
    """Api Backtest History Result

    Args:
        filename (str):
        strategy (str):

    Returns:
        Response[Union[BacktestResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        filename=filename,
        strategy=strategy,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    filename: str,
    strategy: str,
) -> Optional[Union[BacktestResponse, HTTPValidationError]]:
    """Api Backtest History Result

    Args:
        filename (str):
        strategy (str):

    Returns:
        Response[Union[BacktestResponse, HTTPValidationError]]
    """

    return (
        await asyncio_detailed(
            client=client,
            filename=filename,
            strategy=strategy,
        )
    ).parsed
