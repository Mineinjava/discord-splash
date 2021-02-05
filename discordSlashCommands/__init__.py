import asyncio
import websockets
import json

import discordSlashCommands.resources.opcodes as op
import traceback

commands = {}


class Presence():
    def __init__(self, presenceType: int, text: str):
        self.type = presenceType
        self.text = text

    def type(self):
        return self.type

    def text(self):
        return self.text


class ReactionResponse():
    def __init__(self, content: str = None, isEphemeral: bool = False, responseType: int = 4):
        pass

class Member():
    def __init__(self, memberJson):
        self.memberJson = memberJson
    @property
    def avatar(self):
        return self.memberJson['avatar']
    @property
    def id(self):
        return self.memberJson['id']
    @property
    def username(self):
        return self.memberJson['username']
    @property
    def discriminator(self):
        return self.memberJson['id']



class ReactionData():
    def __init__(self, jsonData):
        self.jsonData = jsonData

    @property
    def guild_id(self):
        return self.jsonData["guild_id"]
    @property
    def id(self):
        return self.jsonData['id']
    @property
    def type(self):
        return int(self.jsonData['type'])
    @property
    def user(self):
        return Member(self.jsonData['member']['user'])


class Run():
    """Runs the bot using the token
    parameters:
    token (str): token of the bot to run
    presence: """

    def __init__(self, token: str, presence: Presence = None):
        self.interval = None
        self.sequence = None
        self.session_id = None

        self.TOKEN = token

        self.auth = {
            "token": self.TOKEN,
            "properties": {
                "$os": "windows",
                "$browser": "disco",
                "$device": "disco"
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

        asyncio.run(self.main())
        # asyncio.get_event_loop().run_until_complete(self.hello())
        # print(self.opcode(1, self.sequence))

    async def main(self):
        async with websockets.connect(
                'wss://gateway.discord.gg/?v=6&encoding=json') \
                as self.websocket:
            await self.hello()
            if self.interval is None:
                print("Hello failed, exiting")
                return
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
                elif event_type == "INTERACTION_CREATE":
                    event_name = data['d']['data']['name']
                    try:
                        function = commands[event_name]
                        await function(data)
                    except KeyError:
                        try:
                            raise UnregisteredCommandException(
                                'One or more commands on discord are not represented on this api')
                        except UnregisteredCommandException:
                            traceback.print_exc()

                    # await self.send_message("Editing")

    # async def send_message(self, message):

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


def command(name: str, **options):
    def decorator(func):
        commands[name] = func
        return func

    return decorator


class UnregisteredCommandException(Exception):
    pass
