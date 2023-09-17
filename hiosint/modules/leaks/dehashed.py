from typing import Literal, MutableMapping, Optional

import aiohttp


async def dehashed(
    query: str,
    authorization: str,
    query_type: Literal[
        "email", "ip_address", "username", "password", "hashed_password", "name"
    ] = "email",
    output_var: Optional[MutableMapping] = None,
):
    auth = aiohttp.BasicAuth(*authorization.split("|"))
    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.get(
            "https://api.dehashed.com/search",
            headers={
                "Accept": "application/json",
            },
            params={"query": f'{query_type}:"{query}"'},
        ) as query_resp:
            if query_resp.ok:
                resp_data = await query_resp.json()
                if resp_data.get("success"):
                    if output_var:
                        output_var["dehashed"] = resp_data
                        return
                    else:
                        return resp_data
    return False
