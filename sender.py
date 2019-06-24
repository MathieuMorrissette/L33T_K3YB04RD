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
    async with websockets.connect('ws://192.168.1.66:8766', max_size=None) as websocket:

        authenticated = False

        while not authenticated:
            password = input("Password >")
            
            await websocket.send("CONNECT_SENDER|" + password)

            if(await websocket.recv() == "SUCCESS"):
                authenticated = True


        while(True):
            data_to_send = input("> ")

            if(data_to_send.startswith("PUT|")):
                split = data_to_send.split("|")
                source = split[1]
                destination = split[2]

                f = open(source, "rb")
                data = base64.b64encode(f.read()).decode("utf-8")
                await websocket.send("PUT|" + destination + "|" + data)

                # freeze until transfer done
                await websocket.recv()

            if(data_to_send.startswith("GET|")):
                split = data_to_send.split("|")

                source = split[1]
                destination = split[2]

                await websocket.send("GET|" + source)

                data = base64.b64decode((await websocket.recv()).encode("utf-8"))

                f = open(destination, 'wb')
                f.write(data)
                f.close()
            
            if(data_to_send.startswith("CMD|")):
                await websocket.send(data_to_send)
                print(await websocket.recv())

            if(data_to_send.startswith("SCREEN|")):
                await websocket.send(data_to_send)
                img = b64_2_img((await websocket.recv()).encode("utf-8"))
                img.show()
            

            

asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()