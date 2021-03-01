import asyncio
import websockets
import json
import aiohttp
from enum import Enum
try:
    import opcodes as op  # this will raise an error. Not quite sure why. Please fix. It works fine on PyPi.
    import member
except ModuleNotFoundError:
    from discordSplash import member
    from discordSplash import opcodes as op
import traceback

commands = {}

TOKEN = None
AUTH_HEADER = None
API_URL = 'https://discord.com/api/v8'


class PresenceType(Enum):
    """
    Enumerator for discord PresenceTypes

    Used in the ``presenceType`` parameter for discordSplash.Presence
    """
    Game = 0
    Streaming = 1
    Listening = 2
    Custom = 4
    Competing = 5


class Presence:
    """Presence data used when connecting to Gateway

    :param PresenceType presenceType: type of presence to use.
    :param str text: Text of status to use.

    .. Hint::
        ``x = Presence('a game', discordSplash.PresenceType.Game)``

    .. Warning::
        Streaming URL's currently do not work

        Custom emojis have not been implemented in this API wrapper

        """

    def __init__(self, text: str, presenceType: PresenceType = PresenceType.Game):
        self.type_ = presenceType
        self.text_ = text

    @property
    def type(self):
        """Returns the type of the activity. Used internally

        :return: Integer from 1-5. See class discordSplash.Presence** for more info
        :rtype: int
        """

        return self.type_.value

    @property
    def text(self):
        """Activity Text. Used Internally.

        :return: The text used in the presence.
        :rtype: str
            """
        return self.text_


class InvalidTypeException(Exception):
    """Called when your response is an invalid type.
    """
    pass


class ReactionResponse:
    """
    Base class for responding to an interaction.

    :param str content: Content of the message. Must not be more than 2000 characters.
    :param bool isEphemeral: Whether or not the message should be ephemeral (only seen by the user who created the interaction
    :param int responseType: discord InteractionResponseType

    .. Note::
        [Discord InteractionResponseType](https://discord.com/developers/docs/interactions/slash-commands#interaction-response-interactionresponsetype)

        1	ACK a Ping

        2	ACK a command without sending a message, eating the user's input

        3	respond with a message, eating the user's input

        4	respond with a message, showing the user's input

        5	ACK a command without sending a message, showing the user's input

        "eating" the user's input is recommended for ephemeral commands.

    .. Important::
        TODO:

        - Make ``responseType`` an Enumerator


        """

    def __init__(self, content: str, isEphemeral: bool = False, responseType: int = 4):
        if responseType not in [1, 2, 3, 4, 5]:
            raise InvalidTypeException(
                f"responseType {responseType} is invalid. See https://discord.com/developers/docs/interactions/slash-commands#interaction-response-interactionresponsetype for more info.")
        self.jsonContent = {
            "type": responseType,
            "data": {
                "content": str(content)
            }
        }
        if isEphemeral:
            self.jsonContent['data']['flags'] = 64

    @property
    def json(self):
        """
        Mainly used internally
        :return: JSON content for the reaction
        :rtype: json
        """
        return self.jsonContent


class ReactionData:
    """
    reaction data passed in to the handler

    .. Important::
        TODO:

        - make the choices/parameters better.

    """

    def __init__(self, jsonData):
        self.jsonData = jsonData['d']

    @property
    def guild_id(self):
        """:return: the guild id
        :rtype: str

        .. Important::
            TODO:

            - Make this return a guild object (discordSplash.guild.Guild)

        .. Warning::
            Guilds are not implemented yet.
        """
        return int(self.jsonData["guild_id"])

    @property
    def id(self):
        """:return: the reaction id
        :rtype: str
        """
        return self.jsonData['id']

    @property
    def token(self):
        """:return: the reaction token
        :rtype: str
        .. Caution::
            - Be sure **not to send this in chat. Anyone with the token can send messages as your bot**

            - Expires after 15 minutes
        """
        return self.jsonData['token']

    @property
    def type(self):
        """:return: the reaction type
        :rtype: int

        .. Note ::
            Used for future proofing
            """
        return int(self.jsonData['type'])

    @property
    def member(self):
        """
        :return: a discordSplash.member.Member** object.
        :rtype: discordSplash.member.Member
        """
        return member.Member(self.jsonData['member'])

    @property
    def options(self):
        """
        :return: the choices/parameters for the SlashCommands.
        :rtype: list

        .. Caution::
            Currently returns a list of options. **Is not parsed yet**

        .. Important::
            TODO:

            - parse this
        """
        return self.jsonData['data']['options']

    @property
    def json(self):
        """:return: the JSON. Can be used for a custom parser.
        :rtype: json"""
        return self.jsonData

    async def respond(self, data: ReactionResponse):
        """Responds to the interaction.

        Parameters:

        :param discordSplash.ReactionResponse data: Reaction Response Data

        .. Note::
            This can be called multiple times for followup messages

        .. Important::
            TODO:

            - Add a ``followup`` message function

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


class Run:
    """Runs the bot using the token

    :param str token: token of the bot to run
    :param splash.Presence presence: Presence of the bot, activated upon connection to gateway

    :raises: discordSplash.UnregisteredCommandException

    .. Hint::
        ``Run('TOKEN', Presence(text='testing', presenceType=discordSplash.PresenceType.Game))``

    .. Caution::
        Most of the methods here are only used internally.

    .. Important::
        TODO:

        - Add a ``RESUME``

    .. Danger::
        **Do not share your token with anyone.** If you want to collaborate on a discord bot, use a development team.
    """

    def __init__(self, token: str, presence: Presence = None):
        self.interval = None
        self.sequence = None
        self.session_id = None

        self.TOKEN = token
        global TOKEN, AUTH_HEADER
        TOKEN = token
        AUTH_HEADER = {"Authorization": f"Bot {token}"}


        self.auth = {
            "token": self.TOKEN,
            "properties": {
                "$os": "Python",
                "$browser": "discordSplash",
                "$device": "discordSplash"
            },

        }
        if not presence:
            print('no')
            self.auth['presence'] = {
                "status": "online",
                "afk": False
            }
        else:
            print('has presence ', presence.type, presence.text)

            self.auth['presence'] = {
                "activities": [{
                    "name": presence.text,
                    "type": presence.type
                }],
                "since": 91879201,
                "status": "online",
                "afk": False
            }

        try:
            asyncio.run(self.main(False))
        except websockets.exceptions.ConnectionClosedError:
            while True:
                try:
                    asyncio.run(self.main(True))
                except websockets.exceptions.ConnectionClosedError:
                    pass
        # asyncio.get_event_loop().run_until_complete(self.hello())
        # print(self.opcode(1, self.sequence))

    async def main(self, resume=False):
        async with websockets.connect(
                'wss://gateway.discord.gg/?v=6&encoding=json') \
                as self.websocket:
            if resume is False:
                await self.hello()
                if self.interval is None:
                    print("Hello failed, exiting")
                    return
                await asyncio.gather(self.heartbeat(), self.receive())
            if resume is True:
                await self.resume()
                print('RESUMING------------------------------------------------------------------------------------------------------------------------------------------------')
                await asyncio.gather(self.heartbeat(), self.receive())

            # while self.interval is not None:
            #     pass

    async def receive(self):
        print("Entering receive")
        async for message in self.websocket:
            print("<", message)
            data = json.loads(message)
            if data["op"] == op.DISPATCH:
                self.sequence = int(data["s"])
                event_type = data["t"]
                if event_type == "READY":
                    print('ready')
                    self.session_id = data['d']['session_id']
                elif event_type == "INTERACTION_CREATE":
                    event_name = data['d']['data']['name']
                    try:
                        function = commands[event_name]
                        await function(ReactionData(data))
                    except KeyError:
                        try:
                            raise UnregisteredCommandException(
                                'One or more commands on discord are not represented on this api')
                        except UnregisteredCommandException:
                            traceback.print_exc()

    async def send(self, opcode, payload):
        data = self.opcode(opcode, payload)
        print(">", data)
        await self.websocket.send(data)

    async def heartbeat(self):
        print("Entering heartbeat")
        while self.interval is not None:
            print("Sending a heartbeat")
            await self.send(op.HEARTBEAT, self.sequence)
            await asyncio.sleep(self.interval)

    async def hello(self):
        await self.send(op.IDENTIFY, self.auth)
        print(f"hello > auth")

        ret = await self.websocket.recv()
        print(f"hello < {ret}")

        data = json.loads(ret)
        opcode = data["op"]
        if opcode != 10:
            print("Unexpected reply")
            print(ret)
            return
        self.interval = (data["d"]["heartbeat_interval"] - 2000) / 1000
        # self.interval = 5
        print("interval:", self.interval)

    def opcode(self, opcode: int, payload) -> str:
        data = {
            "op": opcode,
            "d": payload
        }
        return json.dumps(data)

    async def resume(self):
        resume_pkt = await self.create_resume_packet()
        await self.send(op.RESUME, resume_pkt)

    async def create_resume_packet(self):
        resume_blk = {
                "token": self.TOKEN,
                "session_id": self.session_id,
                "seq": self.sequence
            }
        return resume_blk



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


class UnregisteredCommandException(Exception):
    """
    Raised when a command is registered on the Discord API but not on discordSplash.

    .. Important::
        TODO:

        - make it a warning
    """
    pass
