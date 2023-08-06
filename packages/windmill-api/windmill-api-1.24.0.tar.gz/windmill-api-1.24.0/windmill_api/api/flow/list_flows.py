from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    workspace: str,
    page: Union[Unset, int] = UNSET,
    per_page: Union[Unset, int] = UNSET,
    order_desc: Union[Unset, bool] = UNSET,
    created_by: Union[Unset, str] = UNSET,
    path_start: Union[Unset, str] = UNSET,
    path_exact: Union[Unset, str] = UNSET,
    show_archived: Union[Unset, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/w/{workspace}/flows/list".format(client.base_url, workspace=workspace)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "page": page,
        "per_page": per_page,
        "order_desc": order_desc,
        "created_by": created_by,
        "path_start": path_start,
        "path_exact": path_exact,
        "show_archived": show_archived,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _build_response(*, response: httpx.Response) -> Response[None]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    *,
    client: Client,
    workspace: str,
    page: Union[Unset, int] = UNSET,
    per_page: Union[Unset, int] = UNSET,
    order_desc: Union[Unset, bool] = UNSET,
    created_by: Union[Unset, str] = UNSET,
    path_start: Union[Unset, str] = UNSET,
    path_exact: Union[Unset, str] = UNSET,
    show_archived: Union[Unset, bool] = UNSET,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        workspace=workspace,
        page=page,
        per_page=per_page,
        order_desc=order_desc,
        created_by=created_by,
        path_start=path_start,
        path_exact=path_exact,
        show_archived=show_archived,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: Client,
    workspace: str,
    page: Union[Unset, int] = UNSET,
    per_page: Union[Unset, int] = UNSET,
    order_desc: Union[Unset, bool] = UNSET,
    created_by: Union[Unset, str] = UNSET,
    path_start: Union[Unset, str] = UNSET,
    path_exact: Union[Unset, str] = UNSET,
    show_archived: Union[Unset, bool] = UNSET,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        workspace=workspace,
        page=page,
        per_page=per_page,
        order_desc=order_desc,
        created_by=created_by,
        path_start=path_start,
        path_exact=path_exact,
        show_archived=show_archived,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)
