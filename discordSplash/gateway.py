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

import asyncio
import websockets
from . import request
from .presence import UpdatePresence, EmptyUpdatePresence
from .enums import Opcodes
from .events import eventDict
import json


class GatewayBot:
    """
    Bot that connects to Discord's Gateway (Websocket)

    Parameters
    ----------
    token : str
        The bot's token


    Methods
    -------
    run

    Attributes
    ----------
    TOKEN : str
        The bot's token (keep this safe)

    """
    pass

    def __init__(self, token: str, presence: UpdatePresence = EmptyUpdatePresence):

        # stuff for dealing with the gateway
        self._interval = None
        self._sequence = None
        self._session_id = None

        self.CLIENT_ID = None

        self._websocket = None

        self.TOKEN = token
        request.auth_header['Authorization'] = f"Bot {token}"

        TOKEN = self.TOKEN

        self._auth = {
            "token": self.TOKEN,
            "properties": {
                "$os": "Python",
                "$browser": "discordSplash",
                "$device": "discordSplash"
            },
            'presence': presence.to_dict,
            'intents': 29185

        }

    def run(self, update_commands: bool = True):
        """
        Run the bot.
        """

        try:
            asyncio.run(self.connect(resume=False, update_commands=update_commands))
        except websockets.exceptions.ConnectionClosedError:
            while True:
                try:
                    asyncio.run(self.connect(resume=True, update_commands=False))
                except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.ConnectionClosedOK):
                    pass

    async def connect(self, update_commands: bool, resume=False):
        async with websockets.connect(
                'wss://gateway.discord.gg/?v=9&encoding=json') \
                as self._websocket:
            if resume is False:
                await self.hello()
                if self._interval is None:
                    return
                await asyncio.gather(self.heartbeat(), self.receive())
            if resume is True:
                await self.resume()
                print('Reconnecting to discord websocket.')

                await asyncio.gather(self.heartbeat(), self.receive())

            # while self.interval is not None:
            #     pass

    async def receive(self):
        print("Entering receive")
        async for message in self._websocket:
            print("<", message)
            data = json.loads(message)
            if data["op"] == Opcodes.DISPATCH:
                self._sequence = int(data["s"])
                event_type = data["t"]
                if event_type == "READY":
                    print('ready')
                    self.CLIENT_ID = data['d']['user']['id']
                    self._session_id = data['d']['session_id']

                coro = eventDict.get(event_type)
                print("type",data["t"])
                print("coro", coro)
                if coro is not None:
                    await coro(data["d"])
                
                """
                elif event_type == "INTERACTION_CREATE":

                    event_name = data['d']['data']['name']
                    try:
                        function = self.commands[event_name]
                       # await function(ReactionData(data))
                    except:
                        pass
                """

    async def send(self, opcode, payload):
        data = self.opcode(opcode, payload)
        print(">", data)
        await self._websocket.send(data)

    async def heartbeat(self):
        print("Entering heartbeat")
        while self._interval is not None:
            print("Sending a heartbeat")
            await self.send(Opcodes.HEARTBEAT, self._sequence)
            await asyncio.sleep(self._interval)

    async def hello(self):
        await self.send(Opcodes.IDENTIFY, self._auth)
        print(f"hello > auth")

        ret = await self._websocket.recv()
        print(f"hello < {ret}")

        data = json.loads(ret)
        opcode = data["op"]
        if opcode != 10:
            print("Unexpected reply")
            print(ret)
            return
        self._interval = (data["d"]["heartbeat_interval"] - 2000) / 1000
        # self.interval = 5
        print("interval:", self._interval)

    def opcode(self, opcode: int, payload) -> str:
        data = {
            "op": opcode,
            "d": payload
        }
        return json.dumps(data)

    async def resume(self):
        resume_pkt = await self.create_resume_packet()
        await self.send(Opcodes.RESUME, resume_pkt)

    async def create_resume_packet(self):
        resume_blk = {
            "token": self.TOKEN,
            "session_id": self._session_id,
            "seq": self._sequence
        }
        return resume_blk
