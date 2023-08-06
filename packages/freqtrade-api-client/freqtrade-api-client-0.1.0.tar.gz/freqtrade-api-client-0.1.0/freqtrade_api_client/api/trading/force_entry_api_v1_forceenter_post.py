from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.force_enter_payload import ForceEnterPayload
from ...models.http_validation_error import HTTPValidationError
from ...models.status_msg import StatusMsg
from ...models.trade_schema import TradeSchema
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: ForceEnterPayload,
) -> Dict[str, Any]:
    url = "{}/api/v1/forceenter".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[HTTPValidationError, Union[StatusMsg, TradeSchema]]]:
    if response.status_code == 200:

        def _parse_response_200(data: object) -> Union[StatusMsg, TradeSchema]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_force_enter_response_type_0 = TradeSchema.from_dict(data)

                return componentsschemas_force_enter_response_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_force_enter_response_type_1 = StatusMsg.from_dict(data)

            return componentsschemas_force_enter_response_type_1

        response_200 = _parse_response_200(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[HTTPValidationError, Union[StatusMsg, TradeSchema]]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: ForceEnterPayload,
) -> Response[Union[HTTPValidationError, Union[StatusMsg, TradeSchema]]]:
    """Force Entry

    Args:
        json_body (ForceEnterPayload):

    Returns:
        Response[Union[HTTPValidationError, Union[StatusMsg, TradeSchema]]]
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
    json_body: ForceEnterPayload,
) -> Optional[Union[HTTPValidationError, Union[StatusMsg, TradeSchema]]]:
    """Force Entry

    Args:
        json_body (ForceEnterPayload):

    Returns:
        Response[Union[HTTPValidationError, Union[StatusMsg, TradeSchema]]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: ForceEnterPayload,
) -> Response[Union[HTTPValidationError, Union[StatusMsg, TradeSchema]]]:
    """Force Entry

    Args:
        json_body (ForceEnterPayload):

    Returns:
        Response[Union[HTTPValidationError, Union[StatusMsg, TradeSchema]]]
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
    json_body: ForceEnterPayload,
) -> Optional[Union[HTTPValidationError, Union[StatusMsg, TradeSchema]]]:
    """Force Entry

    Args:
        json_body (ForceEnterPayload):

    Returns:
        Response[Union[HTTPValidationError, Union[StatusMsg, TradeSchema]]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
