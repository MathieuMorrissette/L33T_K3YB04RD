import asyncio
import websockets
import keyboard
from io import BytesIO
from PIL import Image
import base64

# Convert Base64 to Image
def b64_2_img(data):
    buff = BytesIO(base64.b64decode(data))
    return Image.open(buff)

async def hello():
    async with websockets.connect('ws://192.168.4.148:8766') as websocket:

        await websocket.send("CONNECT_SENDER")

        while(True):
            data_to_send = input("> ")

            if(data_to_send.startswith("PUT|")):
                split = data_to_send.split("|")
                source = split[1]
                destination = split[2]

                f = open(source, "rb")
                data = base64.b64encode(f.read())
                await websocket.send("PUT|" + destination + "|" + data)

                # freeze until transfer done
                await websocket.recv()
            
            if(data_to_send.startswith("CMD|")):
                await websocket.send(data_to_send)
                print(await websocket.recv())

            if(data_to_send.startswith("SCREEN|")):
                await websocket.send(data_to_send)
                img = b64_2_img(bytes(await websocket.recv()))
                img.show()
            

            

asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()