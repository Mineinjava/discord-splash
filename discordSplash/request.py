# Copyright (C) 2021-Present Mineinjava

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import asyncio

import aiohttp
import typing
from typing import Optional
import time
import warnings
from . import exception, util
from .exception import HTTPexceptionStatusPairing


# will be (hopefully) set when bot connects
# token for the bot.
auth_header: dict = dict()
request_ratelimit_cache: dict = dict()
api_url = "https://discord.com/api/v9"


def get_error_messages(d: dict) -> typing.List[str]:
    """gets all error messages from a flattened json"""
    d = util.flatten(d=d)
    messages = []

    for value in d:
        if isinstance(d[value], list):

            for error in d[value]:
                messages.append(error.get('message'))

    return messages


def get_ratelimit_bucket(**kwargs) -> str:  # channel_id: int = 0, guild_id: int = 0
    """
    Gets a ratelimit bucket including major parameters

    Parameters
    ----------
    channel_id : int
        id of the channel from the ratelimit bucket

    guild_id : int
        id of the guild from the ratelimit bucket

    Returns
    -------
    bucket : str
        the ratelimit bucket from the selected route, channel id, and guild id.
    """
    channel_id = kwargs.get('channel_id', 0)
    guild_id = kwargs.get('guild_id', 0)
    route = kwargs.get('route')
    return f"{route}:{channel_id}:{guild_id}"


async def cleanup_ratelimit(ratelimit_bucket: str, request: aiohttp.ClientResponse) -> None:
    json = {
        "reset": float(request.headers.get('X-RateLimit-Reset', '0')),
        "remaining": int(request.headers.get('X-RateLimit-Remaining', '1'))
    }
    request_ratelimit_cache[ratelimit_bucket] = json
    if not request.ok:
        requestjson = await request.json()
        error_messages = get_error_messages(d=requestjson)

        message = requestjson.get('message', 'no message provided by Discord API')
        message += '\n'.join(error_messages)

        error_to_raise = HTTPexceptionStatusPairing.get(request.status, exception.HTTPWarning)
        raise error_to_raise(message)


async def sleep_ratelimit(bucket):
    """sleeps for the ratelimit based on a certain bucket
    .. SeeAlso
        :func:`get_ratelimit_bucket`"""
    if bucket not in request_ratelimit_cache:
        return

    json: dict = request_ratelimit_cache.get(bucket)
    if json.get("remaining") != 0:
        return

    if json.get('reset') > time.time():
        await asyncio.sleep(time.time()-json.get('reset'))


async def make_request(method, route, json=None, guild_id=0, channel_id=0) -> dict:
    """
    Makes a HTTP request to discord api.

    Generally this will not be used as this package wraps the discord api

    Parameters
    ----------
    method : :class`str`
        HTTP method for the request (``GET``, ``POST``, ``PATCH`` etc...)
    route : :class:`str`
        route to make the api request to

        .. Warning::

            should **not** include the ``https://discord.com/api/v``. *

            *Only include what comes after the ``/`` (including the ``/``)


    json : Optional[:class:`dict`]
        JSON object for the request

    guild_id : Optional[:class:`int`]
        guild id of the request. Used for ratelimit handling

    channel_id : Optional[:class:`int`]
        channel id of the request. Used for ratelimit handling


    Returns
    -------
    dict
        json response body of the request.
    """
    bucket = get_ratelimit_bucket(guild_id=guild_id, channel_id=channel_id)
    await sleep_ratelimit(bucket)
    async with aiohttp.ClientSession(headers=auth_header) as cs:
        async with cs.request(method=method, url=f"{api_url}{route}", json=json) as r:
            await cleanup_ratelimit(ratelimit_bucket=bucket, request=r)

            return await r.json()

