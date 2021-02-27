try:
    from __init__ import AUTH_HEADER as HEADER
    from __init__ import API_URL as URL
    import member
    import channel
except ImportError:
    from discordSplash import AUTH_HEADER as HEADER
    from discordSplash import API_URL as URL
    from discordSplash import member
    from discordSplash import channel
import aiohttp


class Guild:
    """Class for a Discord Guild"""

    def __init__(self, jsondata):
        self.json = jsondata

    @property
    def id(self):
        """
        Returns the Guild's id

        :return: id of the guild represented in this object
        :rtype: int
        """
        return int(self.json['id'])

    @property
    def name(self):
        """
        Returns the name of the guild

        :return: name of guild, without leading or trailing whitespace
        :rtype: str
        """
        return self.json['name']

    @property
    def icon(self):
        """
        Icon hash for the guild

        .. Important::
            TODO:

            - Make an ``icon_url`` property

        :return: Icon hash for the guild
        :rtype: str
        """
        try:
            return self.json['icon']
        except KeyError:
            return None

    @property
    def icon_hash(self):
        """
        Icon hash for the guild if the guild is in a template object

        .. Warning::
            I dont quite understand this. Please open a PR on this

        :return: icon hash of the guild
        :rtype: str
        """
        try:
            return self.json['icon_hash']
        except KeyError:
            return None

    @property
    def invite_splash(self):
        """
        Splash background image for the guild
        Appears when joining a guild from a web browser.

        :return: Image hash for the background image
        :rtype: str
        """
        try:
            return self.json['splash']
        except KeyError:
            return None

    @property
    def discovery_splash(self):
        """
        Discovery Splash hash

        :returns: hash of the Discovery Splash image
        :rtype: str
        """
        try:
            return self.json['discovery_splash']
        except KeyError:
            return None

    @property
    def is_owner(self):
        """
        Is the bot the Guild owner?

        :returns: whether or not the bot is the guild owner
        :rtype: bool
        """
        try:
            return bool(self.json['owner'])
        except KeyError:
            return None

    @property
    def owner_id(self):
        """
        id of the guild owner

        :returns: guild owner's id
        :rtype: int
        """
        try:
            return int(self.json['owner_id'])
        except KeyError:
            return None

    @property
    def permissions(self):
        """
        Permissions for the bot in the guild

        .. Important::
            TODO:

            - make this an ENUM

        :return: Total permissions for the current bot in the guild
        :rtype: str
        """
        try:
            return self.json['permissions']
        except KeyError:
            return None

    @property
    def region(self):
        """
        Voice Region id for the guild

        :return: Region id for the guild
        :rtype: str
        """
        try:
            return self.json['region']
        except KeyError:
            return None

    @property
    def afk_channel(self):
        """
        id of the guild's AFK channel

        :return: AFK channel id
        :rtype: int
        """
        try:
            try:
                return int(self.json['afk_channel_id'])
            except ValueError:
                return self.json['afk_channel_id']
        except KeyError:
            return None

    @property
    def afk_timeout(self):
        """
        Time that it takes to be moved into an AFK channel

        :return: Time, in seconds, of the AFK timeout
        :rtype: int
        """
        try:
            return int(self.json['afk_timeout'])
        except KeyError:
            return None

    @property
    def widget_enabled(self):
        """
        Whether or not the server widget is enabled

        :return: ``True`` if the widget is enabled
        :rtype: bool
        """
        try:
            return bool(self.json['widget_enabled'])
        except KeyError:
            return None

    @property
    def widget_channel_id(self):
        """
        Channel ID that the widget invites to. Returns ``None`` if invite is off

        :return: Channel ID of the widget invite
        :rtype: int
        """
        try:
            try:
                return int(self.json['widget_channel_id'])
            except ValueError:
                return None
        except KeyError:
            return None

    @property
    def verification_level(self):
        """
        Verification level required for the guild

        .. Important::
            TODO:

            - Make it an ENUM

        :return: Verification level required to talk in the guild
        :rtype: int
        """
        try:
            return int(self.json['verification_level'])
        except KeyError:
            return None

    @property
    def explicit_content_filter(self):
        """
        Level of content scanning in the guild

        :return: Level of content scanning and auto-deletion in the guild
        :rtype: int
        """
        try:
            return int(self.json['explicit_content_filter'])
        except KeyError:
            return None

    @property
    def default_message_notifications(self):
        """
        Default message notification level

        .. Important::
            TODO:

            - Make it an ENUM

        :return: Default message notification level for the guild
        :rtype: int

        """
        try:
            return int(self.json['default_message_notifications'])
        except KeyError:
            return None

    @property
    def roles(self):
        """
        List of roles found in the guild

        .. Important::
            TODO:

            - add the discordSplash.guild.role object

        .. Danger::
            This does not work.

        :return: list of discordSplash.guild.Role objects
        :rtype: list
        """

        # try:
        #    return self.json['x']
        # except KeyError:
        #    return None
        return print('This has not been implemented yet')

    @property
    def features(self):
        """
        All features found in the guild

        .. Important::
            TODO:

            - Make it an enum

        :return: a list of guild feature strings
        :rtype: list
        """
        try:
            return self.json['features']
        except KeyError:
            return None

    @property
    def mfa_level(self):
        """
        Required MFA level for the guild

        :return: MFA level for the guild
        :rtype: int
        """
        try:
            return int(self.json['mfa_level'])
        except KeyError:
            return None

    @property
    def owner_app_id(self):
        """
        If the guild creator is a bot, this returns the bot's application ID.

        :return: Guild owner's app id
        :rtype: int
        """
        try:
            try:
                return int(self.json['application_id'])
            except ValueError:
                return None
        except KeyError:
            return None

    @property
    def system_channel_id(self):
        """
        The Channel ID for system messages (member join, boosts).

        :return: System messages channel id
        :rtype: int
        """
        try:
            try:
                return int(self.json['system_channel_id'])
            except ValueError:
                return None
        except KeyError:
            return None

    @property
    def system_channel_flags(self):
        """
        Flags for the System Channel

        :return: System channel's flags
        :rtype: int
        """
        try:
            return int(self.json['system_channel_flags'])
        except KeyError:
            return None

    @property
    def rules_channel(self):
        """
        Channel where community servers post rules

        :return: Channel id of the rules channel
        :rtype: int
        """
        try:
            return int(self.json['x'])
        except KeyError:
            return None

    async def get_preview(self):
        """
        Gets a Guild Preview Object for the guild.

        :return: guild preview object for the guild
        :rtype: discordSplash.guild.GuildPreview
        """
        g_id = self.json['id']
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'{URL}/guilds/{g_id}/preview', headers=HEADER) as r:
                preview = GuildPreview(await r.json())
                return preview

    async def update(self, name: str = None, region: str = None, verification_level: int = None,
                     default_message_notifications: int = None, explicit_content_filter: int = None,
                     afk_channel_id: int = None, afk_timeout: int = None, icon=None, owner_id: str = None,
                     splash=None, banner=None, system_channel_id: int = None, rules_channel_id: int = None,
                     public_updates_channel_id: int = None, preferred_locale: str = None):
        """
        Edits the guild.

        .. Warning::
            Some fields here will not work, depending on the guild. For example:

            - ``owner_id`` only works if the bot is the guild owner
            - ``splash`` and ``banner`` only work if the guild has a level 3 boost or is verified/partnered
            - ``system_channel`` can be disabled

        :param str name: new name of the guild
        :param str region: new voice region of the guild
        :param int verification_level: required verification level for the guild
        :param int default_message_notifications: new message notifications level for the guild
        :param int explicit_content_filter: new explicit content filter for the guild.
        :param int afk_channel_id: new channel ID for the AFK channel
        :param int afk_timeout: new number of seconds a member can be AFK before being moved into an AFK channel
        :param icon: new icon of the guild
        :param str owner_id: id of the new guild owner (bot must be guild owner for this to work.)
        :param splash: new splash image of the guild
        :param banner: new guild banner
        :param int system_channel_id: Channel ID for the system messages channel ID.
        :param int rules_channel_id: channel ids for rules.
        :param int public_updates_channel_id: new channel for moderator info (Discord community updates.)
        :param str preferred_locale: Where the guild is hosted.

        :return: Updated Guild Object
        :rtype: discordSplash.guild.Guild
        """
        json = {"name": name, "region": region, "verification_level": verification_level,
                "default_message_notifications": default_message_notifications,
                "explicit_content_filter": explicit_content_filter, "afk_channel_id": afk_channel_id,
                "afk_timeout": afk_timeout, "icon": icon, "owner_id": owner_id, "splash": splash, "banner": banner,
                "system_channel_id": system_channel_id, "rules_channel_id": rules_channel_id,
                "public_updates_channel_id": public_updates_channel_id, "preferred_locale": preferred_locale}
        for x in json:
            if json[x] is None:
                json.pop(x)

        g_id = self.json['id']
        async with aiohttp.ClientSession() as cs:
            async with cs.patch(f'{URL}/guilds/{g_id}', json=json, headers=HEADER) as r:
                guild_new = Guild(await r.json())
                return guild_new

    async def delete(self):
        """
        deletes the guild

        bot must be guild owner

        .. Danger
            This Permanently deletes the guild.
        """
        g_id = self.json['id']
        async with aiohttp.ClientSession() as cs:
            async with cs.delete(f'{URL}/guilds/{g_id}', headers=HEADER) as r:
                guild_new = Guild(await r.json())
                return guild_new

    async def get_all_channels(self):
        """
        gets all channels in a guild

        :return: list of guild channel objects
        :rtype: [discordSplash.channel.Channel]
        """
        g_id = self.json['id']
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'{URL}/guilds/{g_id}/channels', headers=HEADER) as r:
                channels = []
                for channel_ in await r.json():
                    channels.append(channel.Channel(channel_))

                return channels

    async def create_channel(self, name: str, type: int, topic: str = None, bitrate: int = None, user_limit: int = None,
                             rate_limit_per_user: int = 0, position: int = None, permission_overwrites=None,
                             parent_id: int = None, nsfw: bool = None):
        """
        Creates a channel in the guild.

        .. Tip::
            Some parameters here are only for voice/text channels.

            Only Text:

            - ``topic``
            - ``rate_limit_per_user``

            Only Voice:

            - ``bitrate``
            - ``user_limit``

        :param str name: name of the channel
        :param int type: type of the channel
        :param str topic: Channel topic/description
        :param int bitrate: bitrate (in bits) of the channel
        :param int user_limit: limit for number of users that can join the voice channel
        :param str rate_limit_per_user: cooldown (slowmode) between sending messages
        :param permission_overwrites: permission overwrites for the channel TODO: Implement this
        :param int position: channel order position number
        :param int parent_id: id of the parent channel category
        :param bool nsfw: whether the channel is nsfw or not
        """
        json = {"name": name, "type": type, "bitrate": bitrate,
                "user_limit": user_limit,
                "rate_limit_per_user": rate_limit_per_user, "permission_overwrites": permission_overwrites,
                "position": position, "parent_id": parent_id, "nsfw": nsfw}
        g_id = self.json['id']
        async with aiohttp.ClientSession() as cs:
            async with cs.post(f'{URL}/guilds/{g_id}/channels', json=json, headers=HEADER) as r:
                return channel.Channel(await r.json())

    async def modify_channel_positions(self, data_list: list):
        """
        Adjusts Channel Positions for a guild

        .. Important::
            TODO:

            - make the ``data_list`` parameter better (python object)

        .. Hint::
            the ``data_list`` objects should look something like this:

            .. code-block:: json

                [
                    {
                        "id": 2349892848243,
                        "position": 1
                    },
                    {
                        "id": 7182933290482,
                        "position": 0
                    }
                ]


        :param list data_list: list of json objects for adjusting channel positions. Must be longer than 2.
        :raises: discordSplash.guild.ListLengthError if the ``data_list`` parameter is too short.
        """
        if len(data_list) < 2:
            raise ListLengthError(
                "`data_list` for coroutine discordSplash.guild.modify_channel_positions requires a length of two or more.")
        else:
            g_id = self.json['id']
            async with aiohttp.ClientSession() as cs:
                async with cs.patch(f'{URL}/guilds/{g_id}/channels', json=data_list, headers=HEADER) as r:
                    pass

    async def get_member(self, id_):
        """
        gets a Member from their id

        .. SeeAlso::
            discordSplash.member.Member

            discordSplash.guild.get_all_members()


        :param int id_: ID of the member you want to fetch
        :return: Guild member of the id
        :rtype: discordSplash.member.Member
        """

        g_id = self.json['id']
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'{URL}/guilds/{g_id}/members/{id_}', headers=HEADER) as r:
                member_ = member.Member(await r.json())
                return member_

    async def get_members(self):
        """
        gets all members in a guild

        .. Warning::
            This may be part of privileged intents in the future.

        :return: list of all members found in the guild
        :rtype: [discordSplash.member.Member]
        """
        g_id = self.json['id']
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'{URL}/guilds/{g_id}/members', headers=HEADER) as r:
                members_ = []
                for member_ in await r.json():
                    members_.append(member.Member(member_))
                return members_

    async def modify_member(self, id_, nick: str = None, roles: list = None, mute: bool = None, deaf: bool = None,
                            channel_id: int = None):
        """
        modifies a member of the guild

        .. Hint::
            All of these fields require permission.

        .. Warning::
            If ``channel_id`` is not set, the user will be disconnected from voice.

        :param int id_: id of the member to modify
        :param str nick: new nickname of the member
        :param [list] roles: list of roles the member has
        :param bool mute: whether or not the user is muted
        :param bool deaf: whether or not the user is deafened
        :param str channel_id: id of the voice channel to move the member.

        :return: updated Member object
        :rtype: discordSplash.member.Member
        """
        json = {"nick": nick, "roles": roles, "mute": mute, "deaf": deaf, "channel_id": channel_id}
        g_id = self.json['id']
        async with aiohttp.ClientSession() as cs:
            async with cs.patch(f'{URL}/guilds/{g_id}/members/{id_}', json=json, headers=HEADER) as r:
                member_ = member.Member(r.json)
                return member_


class GuildPreview:
    """
    Guild Preview Object
    """

    def __init__(self, json):
        self.json = json

    @property
    def id(self):
        """
        ID of the guild

        :return: guild id
        :rtype: int
        """
        try:
            return self.json['id']
        except KeyError:
            return None

    @property
    def name(self):
        """
        Guild Name.

        :return: Name of the Guild
        :rtype: str
        """
        try:
            return self.json['name']
        except KeyError:
            return None

    @property
    def icon(self):
        """
        Icon hash of the guild.

        :return: guild icon hash
        :rtype: str
        """
        try:
            return self.json['icon']
        except KeyError:
            return None

    @property
    def splash(self):
        """
        Splash of the guild

        :return: guild splash hash
        :rtype: str
        """
        try:
            return self.json['splash']
        except KeyError:
            return None

    @property
    def discovery_splash(self):
        """
        discovery splash image of the guild

        :return: discovery splash hash
        :rtype: str
        """
        try:
            return self.json['discovery_splash']
        except KeyError:
            return None

    @property
    def emojis(self):
        """
        Emojis found in the Guild

        .. Important::
            TODO:

            - Implement the discordSplash.emoji.Emoji object

        :return: list of discordSplash.emoji.Emoji objects
        :rtype: [discordSplash.emoji.Emoji]
        """
        try:
            return self.json['emojis']
        except KeyError:
            return

    @property
    def features(self):
        """
        Guild Features

        :return: list of guild feature strings
        :rtype: [str]
        """
        try:
            return self.json['features']
        except KeyError:
            return None

    @property
    def approximate_member_count(self):
        """
        Amount of members in the guild.

        :return: Approximate number of members found in the guild
        :rtype: int
        """
        try:
            return int(self.json['approximate_member_count'])
        except KeyError:
            return None

    @property
    def approximate_presence_count(self):
        """
        Amount of online members in the guild.

        :return: Approximate number of online users in the guild
        :rtype: int
        """
        try:
            return int(self.json['approximate_presence_count'])
        except KeyError:
            return None

    @property
    def description(self):
        """
        Guild description

        :return: description of the guild
        :rtype: str
        """
        try:
            return self.json['description']
        except KeyError:
            return None


async def create(name: str, region=None, icon=None, verification_level: int = None,
                 default_message_notifications: int = None,
                 explicit_content_filter: int = None, roles=None, channels=None, afk_channel_id: int = None,
                 afk_timeout: int = None,
                 system_channel_id=None):
    """
    Creates a guild from the given parameters.

    .. SeeAlso::
        many parameters here are also explained in the discordSplash.guild.Guild

    .. Important::
        TODO:

        - make these fields Enums:
            - ``verification_level``
            - ``default_message_notifications``
            - ``explicit_content_filter``
        - add these objects:
            - ``channel``
            - ``role``
        - add an exception if bot is in over 10 guilds
        - add ratelimit handling

    .. Warning::
        this can only be used by bots in less than 10 guilds.

    :param str name: name of the guild
    :param str region: guild region
    :param str icon: icon of the guild
    :param int verification_level: verification level required to participate in the guild
    :param int default_message_notifications: when should users be pinged in the server
    :param int explicit_content_filter: adult content filter for the guild
    :param json roles: role objects for the server
    :param json channels: channel objects for the server
    :param int afk_channel_id: afk channel for the guild
    :param int afk_timeout: seconds until an AFK user is moved to the AFK channel.
    :param int system_channel_id: system channel id for messages such as boosting and users joining
    """
    json = {'name': name}

    if region is not None:
        json['region'] = region

    if icon is not None:
        json['icon'] = icon

    if roles is not None:
        json['roles'] = roles

    if verification_level is not None:
        json['verification_level'] = verification_level

    if default_message_notifications is None:
        json['default_message_notifications'] = default_message_notifications

    if explicit_content_filter is not None:
        json['explicit_content_filter'] = explicit_content_filter

    if channels is not None:
        json['channels'] = channels

    if afk_channel_id is not None:
        json['afk_channel_id'] = afk_channel_id

    if afk_timeout is not None:
        json['afk_timeout'] = afk_timeout

    if system_channel_id is not None:
        json['system_channel_id'] = system_channel_id

    async with aiohttp.ClientSession() as session:
        async with session.post(f'{URL}/guilds', headers=HEADER, json=json) as r:
            guild = Guild(await r.json())
            return guild


async def get(g_id: int, with_counts: bool = False):
    """
    Get a guild from the Guild's id.

    .. Important::
        TODO:

        - add support for ``with_counts`` in the discordSplash.guild.Guild object

    .. Tip::

        .. SeeAlso::
            discordSplash.guild.get_preview()

        If you dont need the discordSplash.guild.Guild object, use the coroutine discordSplash.guild.get_preview.


    :param int g_id: ID of the guild you want to fetch
    :param bool with_counts: If ``True``, ``approximate_presence_count`` and ``approximate_member_count`` will also be returned
    :return: guild object
    :rtype: discordSplash.guild.Guild
    """
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f'{URL}/guilds/{g_id}?with_counts={str(with_counts).lower()}', headers=HEADER) as r:
            guild = Guild(await r.json())
            return guild


async def get_guild_preview(g_id: int):
    """
    Gets a Guild Preview Object.

    :param int g_id: id of the guild
    :return: guild preview object for the guild
    :rtype: discordSplash.guild.GuildPreview
    """
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f'{URL}/guilds/{g_id}/preview', headers=HEADER) as r:
            preview = GuildPreview(await r.json())
            return preview


class ListLengthError(Exception):
    pass
