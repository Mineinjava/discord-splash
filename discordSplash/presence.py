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
from .enums import ActivityType, StatusType
import typing
from typing import Optional


class Activity:
    """
    Discord Activity object

    Parameters
    ----------
    name : :class:`str`
        Name of the activity

    type : Optional[:class:`discord.ActivityType`]
        type of activity. Defaults to ``Game``.

    url : Optional[:class:`str`]
        the stream url. Only used if ``type`` parameter is set to ``Streaming``

    Attributes
    ----------
    to_dict

    name : :class:`str`
        Name of the activity

    type ::class:`discord.ActivityType`
        type of activity.

    url : Optional[:class:`str`]
        the stream url.


    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.name: str = kwargs.get('name')

        if not self.name:
            raise TypeError('Instantiation of Activity missing required parameter ``name``')

        self.type: ActivityType = kwargs.get('type', ActivityType.Game)
        self.url = kwargs.get('url')

    @property
    def to_dict(self):
        """
        converts the activity object to JSON

        Returns
        -------
        json
        """
        return dict(self.kwargs)


class EmptyUpdatePresence:
    """
    An empty activity object

    .. SeeAlso::
        :class:`UpdatePresence`

    """
    to_dict = {"status": "online",
               "afk": False}


class UpdatePresence:
    """
    Sent by the client to indicate a presence or status update.

    .. Warning::
        This is an UpdatePresence object and **does not actually update the client's presence when instantiated.**

    .. Tip::
        Leave the ``afk`` and ``since`` parameters blank most of the time.


    Parameters
    ----------
    activities : List[:class:`discordSplash.Activity`]
        list of activities

    status : :class:`discordSplash.StatusType`
        the bot's new status type

    since: Optional[:class:`int`]
        unix time (in milliseconds) of when the client went idle.

        Optional if the client is not idle

    afk : Optional[:class:`bool`]
        whether or not the client is idle.

    Attributes
    ----------
    activities : List[:class:`discordSplash.Activity`]
        list of activities

    status : :class:`discordSplash.StatusType`
        the bot's new status type

    since: Optional[:class:`int`]
        unix time (in milliseconds) of when the client went idle.

        Optional if the client is not idle

    afk : Optional[:class:`bool`]
        whether or not the client is idle.

    json : dict
        the json of the object.

    """

    def __init__(self, activities: typing.List[Activity], status: StatusType, since: int = None, afk: bool = False):
        self.activities: typing.List[Activity] = activities
        self.status: StatusType = status
        self.since: int = since
        self.afk: bool = afk

        self.to_dict: dict = {
            'since': self.since,
            'activities': [activity.to_dict for activity in self.activities],
            'status': self.status,
            'afk': self.afk
        }
