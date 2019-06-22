# run as root pliz

import asyncio
import websockets
import keyboard
import socket
import time
import subprocess
import pyscreenshot

# looks the first write doesn't work unless we call a function on the module.
keyboard.is_pressed("e")

async def main():
    async with websockets.connect('ws://192.168.4.148:8766') as websocket:
        await websocket.send("CONNECT_RECEIVER")

        while(True):
            print("waiting for server...")
            server = await websocket.recv()

            if(server.startswith("KEY|")):
                keyboard.write(server[4:])
            
            if(server.startswith("CMD|")):
                output = subprocess.getoutput(server[4:])
                await websocket.send("RECEIVER_OUTPUT|" + output)

            if(server.startswith("SCREEN|")):
                im = pyscreenshot.grab()
                await websocket.send("SCREEN|" + im)


            print("writing : " + server)


asyncio.get_event_loop().run_until_complete(main())
asyncio.get_event_loop().run_forever()

