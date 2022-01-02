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

from dataclasses import dataclass
from enum import Enum

from .abstractbaseclass import Object
from .channel import Channel
from .user import User
from .member import Member


class InteractionType(Enum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4


class ComponentType(Enum):
    ACTION_ROW = 1
    BUTTON = 2
    SELECT_MENU = 3


@dataclass(init=False, eq=False)
class Interaction(Object):
    def __init__(self, json):
        self.json = json
        super().__init__(json.get('id'))

        self.application_id = json.get("application_id")
        self.type = InteractionType(json.get("type"))
        self.data = self.json.get("data")
        self.guild_id = self.json.get("guild_id")
        self.channel_id = self.json.get("guild_id")
        self.is_dm = not not not self.guild_id  # whether or not it was sent in a dm
        self.member = Member(self.json.get('member'))
        self.user = User(self.json.get('user'))
        self.invocator = self.member or self.user
        self.token = self.json.get('token')
        self.version = self.json.get('version')


@dataclass(init=False, eq=False)
class InteractionData(Object):
    def __init__(self, json):
        self.json = json
        super().__init__(id=json.get('id'))
        self.name = self.json.get("name")
        self.type = InteractionType(self.json.get("type"))
        self.resolved = self.json.get("resolved")  # TODO: ADD RESOLVED DATA OBJECT
        self.options = self.json.get("options")  # TODO: ADD OPTIONS OBJECT
        self.custom_id = self.json.get("custom_id")
        self.component_type = self.json.get("component_type")  # TODO: ADD COMPONENT TYPE ENUM
        self.values = self.json.get("values")  # TODO: ADD SELECT OPTION VALUES ENUM/CLASS
        self.target_id = int(self.json.get("target_id")) if self.json.get("target_id") is not None else None


@dataclass(init=False)
class InteractionDataOptions:
    def __init__(self, json):
        self.json = json
        self.name = self.json.get("name")
        self.type = self.json.get("type")
        self.value = self.json.get("value")
        self.options = InteractionDataOptions(self.json.get("options")) if self.json.get(
            "options") is not None else None
        self.focused = self.json.get("focused")
