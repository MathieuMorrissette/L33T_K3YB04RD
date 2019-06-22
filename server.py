import asyncio
import websockets
import time
# remember sockets or else they get trashed by the GC
receivers = []
senders = []

async def hello(websocket, path):
        print("waiting to receive clients")
        client_data = await websocket.recv()

        if(client_data == "CONNECT_RECEIVER"):
            receivers.append(websocket)

        elif(client_data == "CONNECT_SENDER"):
            senders.append(websocket)

        while True:
            client_data = await websocket.recv()
            
            if(client_data.startswith("KEY|")):
                await broadcast_key(client_data[4:])




async def broadcast_key(key):
    for client in receivers:            
        await client.send(key)
            
        


start_server = websockets.serve(hello, '192.168.4.148', 8766)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
