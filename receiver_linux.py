# run as root pliz

import asyncio
import websockets
import keyboard
import socket
import time

async def main():
    async with websockets.connect('ws://192.168.4.148:8766') as websocket:
        await websocket.send("CONNECT")

        while(True):
            print("waiting for server...")
            server = await websocket.recv()

            keyboard.write(server)
            print("writing : " + server)


asyncio.get_event_loop().run_until_complete(main())
asyncio.get_event_loop().run_forever()

