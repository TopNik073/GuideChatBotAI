import aiohttp
from aiohttp.client_exceptions import ClientConnectorError

from source.config import Settings


async def get_query(params: dict, endpoint: str) -> tuple[int, dict | None]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"{Settings.URL_TO_API}{endpoint}", params=params) as response:
                return response.status, await response.json()
    except ClientConnectorError as e:
        return 404, e