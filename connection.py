import aiohttp
from aiohttp.client_exceptions import ContentTypeError

async def public_dodo_api(url) -> dict | ContentTypeError:
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url) as response:
            try:
                response = await response.json()
                return response
            except ContentTypeError as e:
                return e
