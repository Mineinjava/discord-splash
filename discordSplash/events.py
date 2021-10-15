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

from typing import Mapping, Coroutine, Any, Callable
from . import exception
slashCommandListenerDict: Mapping[str, Coroutine[Any]] = {}





# InteractionCreateHandler
async def InteractionCreateHandler(data: dict):
    event_name = data['name']
        
    function = slashCommandListenerDict.get(event_name)
    if not function:
        raise exception.SlashCommandNotFound(f"Could not find the slash command named {event_name}")
    else:
        await function()



# MessageCreateHandler
async def MessageCreateHandler(data: dict):
    message = None
    channel = None
    guild   = None
    # dont do this, just wrap the message object
    
    message.id         = data["id"]
    message.author     = data["author"]
    message.timestamp  = data["timestamp"]
    message.content    = data["content"]
    
    channel.id         = data["channel_id"]
    guild.id           = data["guild_id?"]
   


eventDict: Mapping[str, Coroutine[None]] = {
    "INTERACTION_CREATE": InteractionCreateHandler,
    "MESSAGE_CREATE" : MessageCreateHandler
}

