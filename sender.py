import asyncio
import websockets
import keyboard

async def hello():
    async with websockets.connect('ws://localhost:8766') as websocket:
        while(True):
            key = input("> ")

            await websocket.send("KEY|" + key)

asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()