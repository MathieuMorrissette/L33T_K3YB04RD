import asyncio
import websockets
import keyboard

async def hello():
    async with websockets.connect('ws://192.168.4.148:8766') as websocket:

        await websocket.send("CONNECT_SENDER")

        while(True):
            data_to_send = input("> ")

            await websocket.send(data_to_send)
            
            if(data_to_send.startswith("CMD|")):
                print(await websocket.recv())
            

asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()