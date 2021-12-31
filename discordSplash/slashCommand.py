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


import json
from dataclasses import dataclass
import traceback
from typing import Optional

from .abstractbaseclass import Object
from . import enums
from .user import User


@dataclass(init=False, eq=False)
class ReactionResponse:
    """
    Base class for responding to an interaction.

    Parameters
    ---------
    content : str
        Content of the message. Must not be more than 2000 characters.

    isEphemeral : bool
        Whether or not the message should be ephemeral (only seen by the user who created the interaction)

    responseType : discordSplash.enums.InteractionResponseType
        Type of response.

    Attributes
    ----------
    jsonContent : dict
        json of the ReactionResponse.

    

    .. Note::

        The user's input will be shown on all ``responseType``'s unless you set ``isEphemeral`` to ``True``.



        """

    def __init__(self, content: str, isEphemeral: bool = False, responseType: int = 4):
        self.jsonContent = {
            "type": responseType.value,
            "data": {
                "content": str(content)
            }
        }
        if isEphemeral:
            self.jsonContent['data']['flags'] = 64


@dataclass(init=False, eq=False)
class InteractionData():
    """Discord interaction data structure"""

    def __init__(self, type: enums.InteractionType, data: dict):
        self.type: enums.InteractionType = type
        self.data: dict = data


@dataclass(init=False, eq=False)
class Interaction(Object):
    """
    Data about the reaction that will be passed in to interaction listeners.

    .. Admonition:: Operations

        **x == y**

        checks if two Interactions are equal

        **x != y**

        checks if two Interactions are not equal

        **int(x)**

        returns the Interaction's discord id

    Attributes
    ----------
    id
    timestamp
    type : discordSplash.enums.InteractionType
    jsonData : dict
        JSON data for the interaction
    guild_id : Optional[int]


    Methods
    -------

    .. Important::
        TODO: improve ReactionData - make the choices/parameters better.

    """

    def __init__(self, jsonData):
        super.__init__(id=jsonData.get("id"))
        self.jsonData: dict = jsonData
        self.application_id: int = int()
        self.type: enums.InteractionType = enums.InteractionType(
            jsonData.get("type"))

        self.guild_id: Optional[int] = int(jsonData.get("guild_id"))

        # self.guild = (get the guild object)
        self.token: str = jsonData.get("token")
        self.channel_id

        # self.member = (Get Member Somehow)
        self.user: Optional[User] = User(jsonData.get('user'))

        self.data: Optional[InteractionData] = InteractionData(
            jsonData.get("data")) if not not jsonData.get("data") else None

    @property
    def options(self):
        """
        :return: the choices/parameters for the SlashCommands.
        :rtype: list

        .. Caution::
            Currently returns a list of options. **Is not parsed yet**

        """
        options_ = []

        try:
            for x in self.jsonData['data']['options']:
                options_.append(InteractionOption(x))
                return options_
        except KeyError:
            return None
        return options_

    def json(self):
        """
        :return: the JSON. Can be used for a custom parser.
        :rtype: json"""
        return self.jsonData

    async def respond(self, data: ReactionResponse):
        """Responds to the interaction.


        :param discordSplash.ReactionResponse data: Reaction Response Data


        .. Tip::
            This must be called within 3 seconds of receiving the response.

            .. Tip::
                If you do not want to immediately send a message, call this with reactionResponse ResponseType ``1``

            """
        async with aiohttp.ClientSession() as session:
            print("jsondata", self.jsonData)
            async with session.post(
                    f'https://discord.com/api/v8/interactions/{self.jsonData["id"]}/{self.jsonData["token"]}/callback',
                    json=data.json) as resp:
                pass

    async def edit(self, content: ReactionResponse):
        """
        Edits the original reaction response sent.
        :param discordSplash.ReactionResponse content: New content of the reaction response.
        """
        async with aiohttp.ClientSession as session:
            async with session.patch(
                    f'https://discord.com/api/v8/webhooks/{cfg.CLIENT_ID}/{self.jsonData["token"]}/@original',
                    json=content.json) as r:
                pass

    async def send_followup_message(self, data: ReactionResponse):
        """
        send a followup message for that interaction

        :param discordSplash.ReactionResponse data: Content of the followup message.

        .. Important::
            this needs testing.

            - To Test:
                - Ephemeral Messages
        """
        async with aiohttp.ClientSession as session:
            async with session.post(f'https://discord.com/api/v8/webhooks/{cfg.CLIENT_ID}/{self.jsonData["token"]}/',
                                    json=data.json) as r:
                pass

    async def delete_original_response(self):
        """
        delete the original reaction
        """
        async with aiohttp.ClientSession as session:
            async with session.delete(
                    f'https://discord.com/api/v8/webhooks/{cfg.CLIENT_ID}/{self.jsonData["token"]}/@original'):
                pass
    #  TODO: make it possible to edit any message from an interaction - currently it is possible to delete or edit the original response, but not any of the other responses |


def command(name: str):
    """A decorator that is used to register a command.

    :param str name: name of the command

    .. SeeAlso::
        See ``examples`` directory on GitHub for info on usage

    .. Hint::
        Example Code:

        .. code:: python

            @discordSplash.command(name="say-hello")
            async def say_hello(data):
                await data.respond('hi')


    """

    def decorator(func):
        commands[name] = func
        return func

    return decorator


@dataclass(init=False, eq=False)
class InteractionOption:
    """
    Represents the options ('parameters') sent for the command

    .. Tip::
        You **should** check if this is a parameter using InteractionOptions.is_not_subcommand
    """

    def __init__(self, json_):
        self.json = json_

    @property
    def name(self):
        """
        Name of the interaction option

        :return: name of the interaction parameter or subcommand
        :rtype: str
        """
        return self.json['name']

    @property
    def value(self):
        """
        Value of the parameter

        :return: None if it is a subcommand group, or the value of the parameter
        :rtype: Union[int,str,None]
        """
        try:
            return self.json['value']
        except KeyError:
            return None

    @property
    def is_not_subcommand(self):
        """
        Is the option a parameter (not a subcommand)?

        :return: True if this is a parameter, false if this is a subcommand or subcommand group.
        :rtype: bool
        """
        if not self.json['options']:
            return True
        else:
            return False

    @property
    def options(self):
        """
        list of options if this option is a subcommand or subcommand group.

        :return: array of discordSplash.main.InteractionOption (this class)
        :rtype: [discordSplash.main.InteractionOption]
        """
        options__ = []
        try:
            for option in self.json['options']:
                options__.append(InteractionOption(option))
        except KeyError:
            return None
        return options__


class UnregisteredCommandException(Exception):
    """
    Raised when a command is registered on the Discord API but not on discordSplash.

    .. Important::
        TODO:

        - make it a warning
    """
    pass
