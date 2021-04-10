"""
   submodule for making requests to the API.

   Alternatively you could use something like this:

   .. code-block:: python

       async def main():
           async with aiohttp.ClientSession() as session:
               async with session.get('URL', headers=cfg.AUTH_HEADER, json={"your": "JSON", "object": "here"}) as response:
               // Parse the response

   but the methods in this class handle rate limits

   .. Caution::
       as per https://discord.com/developers/docs/topics/rate-limits#invalid-request-limit, it is **strongly recommended** that you handle ratelimits.

       I advise you use these methods rather than aiohttp as these automatically parse ratelimits.


"""

import asyncio
import time
import aiohttp
from .cfg import AUTH_HEADER as HEADER

routes = {}
guild_ids = {}
channel_ids = {}


async def ratelimit_sleeper(route: str, channel_id: int = None, guild_id: int = None):
    """
    Sleep the amount of time remaining on that route/guild/channel

    Mainly used internally.
    """
    if not channel_id:
        if not guild_id:
            if routes[route]['remaining'] == 0:
                pass
            else:
                await asyncio.sleep(routes[route]['epoch'] - int(time.time()))

        elif not guild_id in guild_ids:
            pass
        else:
            if guild_ids[guild_id]['remaining'] == 0:
                pass
            else:
                await asyncio.sleep(guild_ids[guild_id]['epoch'] - int(time.time()))
    elif not channel_id in channel_ids:
        pass
    else:
        if channel_ids[channel_id]['remaining'] == 0:
            pass
        else:
            await asyncio.sleep(channel_ids[channel_id]['epoch'] - int(time.time()))


async def ratelimit_cleanup(epoch, remaining, channel_id, guild_id, route):
    """
    Used to set the JSON dicts for the channel/guild/http route

    .. Caution::
        Tampering with this *could* lead to ``429`` responses

    This will always be overridden on the next HTTP request
    """
    if not channel_id:
        if not guild_id:
            routes[route]['remaining'] = int(remaining)
            routes[route]['epoch'] = int(epoch)
        else:
            guild_ids[guild_id]['remaining'] = int(remaining)
            guild_ids[guild_id]['epoch'] = int(epoch)
    else:
        channel_ids[channel_id]['remaining'] = int(remaining)
        channel_ids[channel_id]['epoch'] = int(epoch)


# all json formats above take into account the requests_remaining as "remaining" and epoch reset seconds as "epoch"


async def get(route: str, channel_id: int = None, guild_id: int = None):
    """
    Makes a HTTP ``GET`` request to discord's api

    :param str route: route to make the request to
    :param int channel_id: id of the channel you want to modify
    :param int guild_id: id of the guild you want to modify

    .. Tip::
        use either ``channel_id`` or ``guild_id``. **Not Both**

    """
    await ratelimit_sleeper(route, channel_id, guild_id)
    async with aiohttp.ClientSession() as session:
        async with session.get(route, headers=HEADER) as response:
            head = response.headers
            ech = head['X-RateLimit-Reset']
            rm = head['X-RateLimit-Remaining']
            await asyncio.create_task(
                ratelimit_cleanup(epoch=ech, remaining=rm, channel_id=channel_id, route=route, guild_id=guild_id))
            return await response.json()


async def post(route, channel_id=None, guild_id=None, json=None):
    """
    Makes a HTTP ``POST`` request to discord's api

    :param str route: route to make the request to
    :param int channel_id: id of the channel you want to modify
    :param int guild_id: id of the guild you want to modify
    :param json json: json of the request body

    .. Tip::
        use either ``channel_id`` or ``guild_id``. **Not Both**

    """
    await ratelimit_sleeper(route, channel_id, guild_id)
    if not json:
        async with aiohttp.ClientSession() as session:
            async with session.post(route, headers=HEADER) as response:
                head = response.headers
                ech = head['X-RateLimit-Reset']
                rm = head['X-RateLimit-Remaining']
                await asyncio.create_task(
                    ratelimit_cleanup(epoch=ech, remaining=rm, channel_id=channel_id, route=route, guild_id=guild_id))
                return await response.json()
    else:
        async with aiohttp.ClientSession() as session:
            async with session.post(route, headers=HEADER, json=json) as response:
                head = response.headers
                ech = head['X-RateLimit-Reset']
                rm = head['X-RateLimit-Remaining']
                await asyncio.create_task(
                    ratelimit_cleanup(epoch=ech, remaining=rm, channel_id=channel_id, route=route, guild_id=guild_id))
                return await response.json()


async def patch(route, channel_id=None, guild_id=None, json=None):
    """
    Makes a HTTP ``PATCH`` request to discord's api

    :param str route: route to make the request to
    :param int channel_id: id of the channel you want to modify
    :param int guild_id: id of the guild you want to modify
    :param json json: json of the request body

    .. Tip::
        use either ``channel_id`` or ``guild_id``. **Not Both**

    """
    await ratelimit_sleeper(route, channel_id, guild_id)
    if not json:
        async with aiohttp.ClientSession() as session:
            async with session.patch(route, headers=HEADER) as response:
                head = response.headers
                ech = head['X-RateLimit-Reset']
                rm = head['X-RateLimit-Remaining']
                await asyncio.create_task(
                    ratelimit_cleanup(epoch=ech, remaining=rm, channel_id=channel_id, route=route, guild_id=guild_id))
                return await response.json()
    else:
        async with aiohttp.ClientSession() as session:
            async with session.patch(route, headers=HEADER, json=json) as response:
                head = response.headers
                ech = head['X-RateLimit-Reset']
                rm = head['X-RateLimit-Remaining']
                await asyncio.create_task(
                    ratelimit_cleanup(epoch=ech, remaining=rm, channel_id=channel_id, route=route, guild_id=guild_id))
                return await response.json()


async def delete(route, channel_id=None, guild_id=None):
    """
    Makes a HTTP ``DELETE`` request to discord's api

    :param str route: route to make the request to
    :param int channel_id: id of the channel you want to modify
    :param int guild_id: id of the guild you want to modify

    .. Tip::
        use either ``channel_id`` or ``guild_id``. **Not Both**

    """
    await ratelimit_sleeper(route, channel_id, guild_id)

    async with aiohttp.ClientSession() as session:
        async with session.delete(route, headers=HEADER) as response:
            head = response.headers
            ech = head['X-RateLimit-Reset']
            rm = head['X-RateLimit-Remaining']
            await asyncio.create_task(
                ratelimit_cleanup(epoch=ech, remaining=rm, channel_id=channel_id, route=route, guild_id=guild_id))
            return await response.json()


async def put(route, channel_id=None, guild_id=None, json=None):
    """
    Makes a HTTP ``PUT`` request to discord's api

    :param str route: route to make the request to
    :param int channel_id: id of the channel you want to modify
    :param int guild_id: id of the guild you want to modify
    :param json json: json of the request body

    .. Tip::
        use either ``channel_id`` or ``guild_id``. **Not Both**

    """
    await ratelimit_sleeper(route, channel_id, guild_id)
    if not json:
        async with aiohttp.ClientSession() as session:
            async with session.patch(route, headers=HEADER) as response:
                head = response.headers
                ech = head['X-RateLimit-Reset']
                rm = head['X-RateLimit-Remaining']
                await asyncio.create_task(
                    ratelimit_cleanup(epoch=ech, remaining=rm, channel_id=channel_id, route=route, guild_id=guild_id))
                return await response.json()
    else:
        async with aiohttp.ClientSession() as session:
            async with session.patch(route, headers=HEADER, json=json) as response:
                head = response.headers
                ech = head['X-RateLimit-Reset']
                rm = head['X-RateLimit-Remaining']
                await asyncio.create_task(
                    ratelimit_cleanup(epoch=ech, remaining=rm, channel_id=channel_id, route=route, guild_id=guild_id))
                return await response.json()
