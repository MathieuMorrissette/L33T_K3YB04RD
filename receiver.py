import asyncio
import websockets
import keyboard

async def main():
    print("connecting...")
    async with websockets.connect('ws://localhost:8766')as websocket:
        await websocket.send("CONNECT")

        while(True):
            print("waiting for server...")
            server = await websocket.recv()
            keyboard.write(server)
            print(server)

asyncio.get_event_loop().run_until_complete(main())
asyncio.get_event_loop().run_forever()
