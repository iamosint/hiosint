from asyncio import create_task
from random import choice
from typing import MutableMapping, Optional

from duckduckgo_search import DDGS


async def _duckduckgo_search(target: str, output_var: Optional[MutableMapping] = None):
    urls = set()
    with DDGS() as search:
        for result in search.text(
            f'"{target}"',
            region="us-en",
            safesearch="off",
            backend=choice(("api", "html", "lite")),
        ):
            urls.add(result.get("href"))
    if output_var:
        output_var["duckduckgo"] = list(urls)
    return list(urls)


async def duckduckgo(target: str, output_var: Optional[MutableMapping] = None):
    return await create_task(_duckduckgo_search(target, output_var))
