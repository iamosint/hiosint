from typing import MutableMapping, Optional

from aiohttp import ClientSession


async def snusbase(
    target: str, activation_code: str, output_var: Optional[MutableMapping] = None
):
    async with ClientSession() as session:
        async with session.post(
            "https://api.snusbase.com/data/search",
            headers={
                "Content-Type": "application/json",
                "Auth": activation_code,
            },
            json={
                "terms": [target],
                "types": ["email"],
                "wildcard": False,
            },
        ) as snusbase_request:
            if snusbase_request.ok:
                if resp_data := await snusbase_request.json():
                    if output_var:
                        output_var["snusbase"] = resp_data
                        return
                    else:
                        return resp_data
    return False
