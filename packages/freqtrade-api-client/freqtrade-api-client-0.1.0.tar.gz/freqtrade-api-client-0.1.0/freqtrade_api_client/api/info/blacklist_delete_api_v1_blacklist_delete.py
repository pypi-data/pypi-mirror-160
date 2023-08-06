from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.blacklist_response import BlacklistResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    pairs_to_delete: Union[Unset, None, List[str]] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/blacklist".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_pairs_to_delete: Union[Unset, None, List[str]] = UNSET
    if not isinstance(pairs_to_delete, Unset):
        if pairs_to_delete is None:
            json_pairs_to_delete = None
        else:
            json_pairs_to_delete = pairs_to_delete

    params["pairs_to_delete"] = json_pairs_to_delete

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
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
    pairs_to_delete: Union[Unset, None, List[str]] = UNSET,
) -> Response[Union[BlacklistResponse, HTTPValidationError]]:
    """Blacklist Delete

     Provide a list of pairs to delete from the blacklist

    Args:
        pairs_to_delete (Union[Unset, None, List[str]]):

    Returns:
        Response[Union[BlacklistResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        pairs_to_delete=pairs_to_delete,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    pairs_to_delete: Union[Unset, None, List[str]] = UNSET,
) -> Optional[Union[BlacklistResponse, HTTPValidationError]]:
    """Blacklist Delete

     Provide a list of pairs to delete from the blacklist

    Args:
        pairs_to_delete (Union[Unset, None, List[str]]):

    Returns:
        Response[Union[BlacklistResponse, HTTPValidationError]]
    """

    return sync_detailed(
        client=client,
        pairs_to_delete=pairs_to_delete,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    pairs_to_delete: Union[Unset, None, List[str]] = UNSET,
) -> Response[Union[BlacklistResponse, HTTPValidationError]]:
    """Blacklist Delete

     Provide a list of pairs to delete from the blacklist

    Args:
        pairs_to_delete (Union[Unset, None, List[str]]):

    Returns:
        Response[Union[BlacklistResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        pairs_to_delete=pairs_to_delete,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    pairs_to_delete: Union[Unset, None, List[str]] = UNSET,
) -> Optional[Union[BlacklistResponse, HTTPValidationError]]:
    """Blacklist Delete

     Provide a list of pairs to delete from the blacklist

    Args:
        pairs_to_delete (Union[Unset, None, List[str]]):

    Returns:
        Response[Union[BlacklistResponse, HTTPValidationError]]
    """

    return (
        await asyncio_detailed(
            client=client,
            pairs_to_delete=pairs_to_delete,
        )
    ).parsed
