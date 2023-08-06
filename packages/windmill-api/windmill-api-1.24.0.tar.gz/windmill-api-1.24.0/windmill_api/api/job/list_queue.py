import datetime
from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    workspace: str,
    order_desc: Union[Unset, bool] = UNSET,
    created_by: Union[Unset, str] = UNSET,
    parent_job: Union[Unset, str] = UNSET,
    script_path_exact: Union[Unset, str] = UNSET,
    script_path_start: Union[Unset, str] = UNSET,
    script_hash: Union[Unset, str] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    success: Union[Unset, bool] = UNSET,
    job_kinds: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/w/{workspace}/jobs/queue/list".format(client.base_url, workspace=workspace)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_created_before: Union[Unset, str] = UNSET
    if not isinstance(created_before, Unset):
        json_created_before = created_before.isoformat()

    json_created_after: Union[Unset, str] = UNSET
    if not isinstance(created_after, Unset):
        json_created_after = created_after.isoformat()

    params: Dict[str, Any] = {
        "order_desc": order_desc,
        "created_by": created_by,
        "parent_job": parent_job,
        "script_path_exact": script_path_exact,
        "script_path_start": script_path_start,
        "script_hash": script_hash,
        "created_before": json_created_before,
        "created_after": json_created_after,
        "success": success,
        "job_kinds": job_kinds,
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
    order_desc: Union[Unset, bool] = UNSET,
    created_by: Union[Unset, str] = UNSET,
    parent_job: Union[Unset, str] = UNSET,
    script_path_exact: Union[Unset, str] = UNSET,
    script_path_start: Union[Unset, str] = UNSET,
    script_hash: Union[Unset, str] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    success: Union[Unset, bool] = UNSET,
    job_kinds: Union[Unset, str] = UNSET,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        workspace=workspace,
        order_desc=order_desc,
        created_by=created_by,
        parent_job=parent_job,
        script_path_exact=script_path_exact,
        script_path_start=script_path_start,
        script_hash=script_hash,
        created_before=created_before,
        created_after=created_after,
        success=success,
        job_kinds=job_kinds,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: Client,
    workspace: str,
    order_desc: Union[Unset, bool] = UNSET,
    created_by: Union[Unset, str] = UNSET,
    parent_job: Union[Unset, str] = UNSET,
    script_path_exact: Union[Unset, str] = UNSET,
    script_path_start: Union[Unset, str] = UNSET,
    script_hash: Union[Unset, str] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    success: Union[Unset, bool] = UNSET,
    job_kinds: Union[Unset, str] = UNSET,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        workspace=workspace,
        order_desc=order_desc,
        created_by=created_by,
        parent_job=parent_job,
        script_path_exact=script_path_exact,
        script_path_start=script_path_start,
        script_hash=script_hash,
        created_before=created_before,
        created_after=created_after,
        success=success,
        job_kinds=job_kinds,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)
