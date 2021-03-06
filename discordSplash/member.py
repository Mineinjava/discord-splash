import aiohttp
import os.path
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from cfg import AUTH_HEADER as HEADER
from main import API_URL as URL



class User:
    """Represents a discord member. Used internally to parse interaction/member JSON data.

    :param json memberJson: JSON to parse into this class.

    .. Important::
        TODO: support sernding dms to user - add a method to send a DM to the user on the user object

        TODO: Support avatar urls for Users - add an `avatar_url` property in the User class"""

    def __init__(self, memberJson):
        self.memberJson = memberJson

    @property
    def avatar(self):
        """
        :return: the member's avatar hash
        :rtype: str
        .. Important::
            TODO:

            - make it an ``avatar_url`` or make that a separate property

        """
        return self.memberJson['avatar']

    @property
    def id(self):
        """
        :return: the user's id
        :rtype: int
        """
        return int(self.memberJson['id'])

    @property
    def username(self):
        """
        :return: the user's username
        :rtype: str
        """
        return self.memberJson['username']

    @property
    def discriminator(self):
        """
        :return: the user's discriminator
        :rtype: int
        """

        return int(self.memberJson['discriminator'])


class Member:
    """
    Discord Guild Member Object.

    Contains the discordSplash.member.User object but this class has additional support for roles and other guild specific data.

    .. SeeAlso::
        - Also known as a Guild Member
        - discordSplash.member.User
    """

    def __init__(self, json):
        self.json = json

    @property
    def user(self):
        """
        Discord user that is in the guild

        :return: discordSplash.member.User object
        :rtype: discordSplash.member.User
        """
        try:
            return User(self.json['user'])
        except KeyError:
            return None

    @property
    def nickname(self):
        """
        Nickname of the user

        :return: Member's nickname
        :rtype: str
        """
        try:
            return self.json['user']
        except KeyError:
            return None

    @property
    def roles(self):
        """
        The Member's Roles

        .. Important::
            TODO:

            - add the Role object

        :return: a list of all of the member's role ids
        :rtype: [int]
        """
        try:
            return self.json['roles']
        except KeyError:
            return None

    @property
    def joined_at(self):
        """
        When the member joined the guild

        :return: ISO8601 Timestamp
        :rtype: str
        """
        try:
            return self.json['joined_at']
        except KeyError:
            return None

    @property
    def guild_id(self):
        """
        ID of the Guild the member is in
        :return: Guild ID
        :rtype: int
        """
        try:
            return int(self.json['guild_id'])
        except KeyError:
            return None

    @property
    def premium_since(self):
        """
        When the member began boosting the guild

        :return: ISO8601 Timestamp
        :rtype: str
        """
        try:
            return self.json['premium_since']
        except KeyError:
            return None

    @property
    def deaf(self):
        """
        Whether or not the user is deafened in the guild

        :return: True if the user is deafened
        :rtype: bool
        """
        try:
            return bool(self.json['deaf'])
        except KeyError:
            return None

    @property
    def mute(self):
        """
        Whether or not the user is muted in the guild

        :return: True if the user is muted
        :rtype: bool
        """
        try:
            return bool(self.json['mute'])
        except KeyError:
            return None

    @property
    def pending(self):
        """
        Whether or not the member has passed the membership screening

        :return: False if the member has passed the screening
        :rtype: bool
        """
        try:
            return bool(self.json['pending'])
        except KeyError:
            return None

    @property
    def permissions(self):
        """
        Total permissions of the member in the channel

        .. Tip::
            This includes channel overrides

        .. Note::
            This only is used during the ``INTERACTION_CREATE`` Gateway event.

        :return:
        :rtype:
        """
        try:
            return self.json['']
        except KeyError:
            return None

    async def update(self, guild_id, nick: str = None, roles: list = None, mute: bool = None, deaf: bool = None,
                     channel_id: int = None):
        """
        modifies the guild member object

        .. Hint::
            All of these fields require permission.

            All of these fields are optional

        .. Warning::
            If ``channel_id`` is not set, the user will be disconnected from voice.

        .. SeeAlso::
            coroutine discordSplash.guild.Guild.modify_member()

        :param str nick: new nickname of the member
        :param [list] roles: list of roles the member has
        :param bool mute: whether or not the user is muted
        :param bool deaf: whether or not the user is deafened
        :param str channel_id: id of the voice channel to move the member.

        :return: updated Member object
        :rtype: discordSplash.member.Member
        """
        json = {"nick": nick, "roles": roles, "mute": mute, "deaf": deaf, "channel_id": channel_id}
        g_id = guild_id
        id_ = self.json['user']['id']
        async with aiohttp.ClientSession() as cs:
            async with cs.patch(f'{URL}/guilds/{g_id}/members/{id_}', json=json, headers=HEADER) as r:
                member_ = Member(r.json)
                print(HEADER)
                print(r)
                return member_
