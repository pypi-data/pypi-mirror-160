from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.plot_config import PlotConfig
from ...models.plot_config_type_1 import PlotConfigType1
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/v1/plot_config".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[PlotConfig, PlotConfigType1]]:
    if response.status_code == 200:

        def _parse_response_200(data: object) -> Union[PlotConfig, PlotConfigType1]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_plot_config_type_0 = PlotConfig.from_dict(data)

                return componentsschemas_plot_config_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_plot_config_type_1 = PlotConfigType1.from_dict(data)

            return componentsschemas_plot_config_type_1

        response_200 = _parse_response_200(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[PlotConfig, PlotConfigType1]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[PlotConfig, PlotConfigType1]]:
    """Plot Config

    Returns:
        Response[Union[PlotConfig, PlotConfigType1]]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[PlotConfig, PlotConfigType1]]:
    """Plot Config

    Returns:
        Response[Union[PlotConfig, PlotConfigType1]]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[PlotConfig, PlotConfigType1]]:
    """Plot Config

    Returns:
        Response[Union[PlotConfig, PlotConfigType1]]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[PlotConfig, PlotConfigType1]]:
    """Plot Config

    Returns:
        Response[Union[PlotConfig, PlotConfigType1]]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
