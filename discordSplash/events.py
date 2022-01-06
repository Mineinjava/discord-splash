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

from typing import Mapping, Awaitable, Any, Callable
import multidict

from . import exception
from .message import Message

eventdict = multidict.MultiDict()


# InteractionCreateHandler
async def InteractionCreateHandler(data: dict, out_func):
    """
    Handles an Interaction_Create event
    """
    event_name = data['name']


async def MessageCreateHandler(data: dict, out_func):
    message = Message(data)
    await out_func(message)


def eventListener(event_name):
    """decorator that makes a coroutine listen for an event"""

    def wrapper(func):
        eventdict.add(event_name, func)
        print(event_name, func)

    return wrapper


async def eventHandler(event_type, data, out_func):
    func = i_eventDict.get(event_type)
    if func is not None:
        await func(data, out_func)


i_eventDict = {
    "INTERACTION_CREATE": InteractionCreateHandler,
    "MESSAGE_CREATE": MessageCreateHandler
}
