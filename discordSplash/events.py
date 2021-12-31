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

from . import exception
from .message import Message

slashCommandListenerDict: Mapping[str, Awaitable[Any]] = {}


# InteractionCreateHandler
async def InteractionCreateHandler(data: dict):
    """
    Handles an Interaction_Create event
    """
    event_name = data['name']

    function = slashCommandListenerDict.get(event_name)
    if not function:
        raise exception.SlashCommandNotFound(f"Could not find the slash command named {event_name}")
    else:
        await function()


messageListenerDict = []


# MessageCreateHandler
async def MessageCreateHandler(data: dict):
    messageListener(data)
    message = Message(data)
    for ls in messageListenerDict:
        print(messageListenerDict)
        await ls(message)


def messageListener(func):
    """Decorator that adds a messageListener to an object."""
    print("func", func)
    if not isinstance(func, dict):
        messageListenerDict.append(func)

    def wrapper():
        pass


eventDict = {
    "INTERACTION_CREATE": InteractionCreateHandler,
    "MESSAGE_CREATE": MessageCreateHandler
}
