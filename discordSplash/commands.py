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
from typing import Awaitable, List, Optional

from .enums import ApplicationCommandOptionType


class ApplicationCommandOption:
    """
    Represents a discord Application Command Option

    .. Warn::
        ``choices`` are not yet supported.

    Parameters
    ----------
    type : :class:`discordSplash.ApplicationCommandOptionType`
        Type of the command Option

    name : :class:`str`
        Name of the option

    description : :class:`str`
        Description of the option

    required : Optional[:class:`bool`]
        Whether or not the option is required.

    options : Optional[List[:class:`ApplicationCommandOption`]]
        List of options if this option is a subcommand or subcommand group.


    Attributes
    ----------
    to_dict

    type : :class:`discordSplash.ApplicationCommandOptionType`
        Type of the command Option

    raw_type : :class:`int`
        the integer that represents the option type.

    name : :class:`str`
        Name of the option

    description : :class:`str`
        Description of the option

    required : Optional[:class:`bool`]
        Whether or not the option is required. Defaults to :class:`False`

    options : Optional[List[:class:`ApplicationCommandOption`]]
        List of options if this option is a subcommand or subcommand group.

    """

    def __init__(self, type: ApplicationCommandOptionType, name: str, description: str, **kwargs):
        self.type = type
        self.raw_type = type.value
        self.name = name
        self.description = description
        self.required = kwargs.get('required', False)
        self.options = kwargs.get('options')
        self._kwargs = kwargs

    @property
    def to_dict(self) -> dict:
        """turns the :class:`ApplicationCommandOption` into a JSON dict"""
        dict = dict(self._kwargs)
        dict['type'] = self.raw_type
        dict['name'] = self.name
        dict['description'] = self.description

        return dict


class Command:
    """class that represents a slash command.

    This is what is being sent when the slash commands are being created."""

    def __init__(self, coro: Awaitable, name:str, description:str, **kwargs):
        self.callback = coro
