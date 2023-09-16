from asyncio import create_task
from typing import MutableMapping, Optional

from googlesearch import search


async def _google_search(target: str, output_var: Optional[MutableMapping] = None):
    urls = set()
    for result in search(f'"{target}"'):
        urls.add(result)
    if output_var:
        output_var["google"] = list(urls)
    return list(urls)


async def google(target: str, output_var: Optional[MutableMapping] = None):
    return await create_task(_google_search(target, output_var))
