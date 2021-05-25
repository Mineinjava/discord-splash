"""
Copyright (C) 2021-Present Mineinjava

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import asyncio
from . import request


class GatewayBot:
    """
    Bot that connects to Discord's Gateway (Websocket)
    """

    def __init__(self, token: str, presence: Presence = None):
        # stuff for dealing with the gateway
        self.interval = None
        self.sequence = None
        self.session_id = None

        self.TOKEN = token
        request.auth_header ['']

        cfg.AUTH_HEADER = {"Authorization": f"Bot {token}"}
        ratelimit.HEADER = {"Authorization": f"Bot {token}"}
        TOKEN = self.TOKEN
        print('header 1', cfg.AUTH_HEADER)

        self.auth = {
            "token": self.TOKEN,
            "properties": {
                "$os": "Python",
                "$browser": "discordSplash",
                "$device": "discordSplash"
            },

        }
        if not presence:
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
                except websockets.exceptions.ConnectionClosedOK:
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
                print('RESUMING--------------------------------')

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
                    cfg.CLIENT_ID = data['d']['user']['id']
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
