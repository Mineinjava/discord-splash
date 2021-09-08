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
"""
DiscordSplash Enumterators.
"""
from enum import Enum


class Opcodes:
    """Discord gateway opcodes"""
    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    STATUS_UPDATE = 3
    VOICE_UPDATE = 4
    RESUME = 6
    RECONNECT = 7
    REQUEST_MEMBERS = 8
    INVALID_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11


class ApplicationCommandOptionType(Enum):
    """
    Enumerator for discord Slash command option types.
    """
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9


class ActivityType(Enum):
    """
    Enumerator for discord Activity Types
    """
    Game = 0
    Streaming = 1
    Listening = 2
    Custom = 4
    Competing = 5


class StatusType(Enum):
    """
    Enumerator for Discord status types
    """
    online = 'online'
    dnd = 'dnd'
    afk = 'idle'
    invisible = 'invisible'
    offline = 'offline'
