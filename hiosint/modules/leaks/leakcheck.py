from typing import Literal, MutableMapping, Optional

from aiohttp import ClientSession


async def leakcheck(
    target: str,
    api_key: str,
    query_type: Literal["auto", "email", "login"] = "auto",
    output_var: Optional[MutableMapping] = None,
):
    async with ClientSession() as session:
        async with session.get(
            "https://leakcheck.net/api",
            params={
                "key": api_key,
                "check": target,
                "type": query_type if query_type else "auto",
            },
        ) as leakcheck_request:
            if leakcheck_request.ok:
                if (resp_data := await leakcheck_request.json()).get("success", False):
                    if output_var:
                        output_var["leakcheck"] = resp_data
                    else:
                        return resp_data
    return False
