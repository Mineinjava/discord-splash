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

import typing
from typing import Optional, Union
from .abstractbaseclass import Object


class User(Object):
    """
    Represents a Discord user

    Not to be confused with discordSplash.user.Member

    .. Admonition:: Operations

        **x == y**

        checks if two users are equal

        **x != y**

        checks if two users are not equal

        **int(x)**

        returns the user's discord id

        **str(x)**

        returns the user's username and discriminator

    Parameters
    ----------
    json : dict
        JSON of user data to be passed in to the object

    Attributes
    ----------
    id : :class:`int`
        the id of the user

    username : :class:`str`
        the user's username

    discriminator : :class:`int`
        the user's 4-digit discriminator

    avatar : Optional[:class:`str`]
        the user's avatar hash. Can be ``None`` if the user has no avatar.

    bot : :class:`bool`
        whether or not the user is a bot

    system : :class:`bool`
        whether or not the user is an Official Discord System user

    mfa_enabled : Optional[:class:`bool`]
        whether or not the user has multi-factor auth (MFA) enabled on their account

    locale : Optional[:class:`str`]
        the user's chosen language.
        ``None`` unless the user retrieved through Oauth2

    verified : Optional[:class:`bool`]
        whether or not the user's email account is verified
        ``None`` unless the user is retrieved through Oauth2

    flags : Optional[:class:`int`]
        the flags on a user's account

    premium_type : Optional[:class:`int`]
        the type of nitro subscription on a user's account

    public_flags : Optional[:class:`int`]
        the public flags on a user's account

    timestamp : :class:`datetime.datetime`
        timestamp of when the object was created.


    Methods
    -------

    """

    def __init__(self, json):
        super().__init__(json.get('id'))
        self._json          = json
        self.username       = json.get("username")
        self.discriminator  = json.get("discriminator")
        self.avatar         = json.get('avatar')
        self.bot            = json.get('bot', False)
        self.mfa_enabled    = json.get('mfa_enabled')
        self.system         = json.get('system', False)
        self.locale         = json.get('locale')
        self.verified       = json.get('verified')
        self.flags          = json.get('flags')
        self.premium_type   = json.get('premium_type')
        self.public_flags   = json.get('public_flags')

    def __str__(self):
        return f"{self.username}#{self.discriminator}"
