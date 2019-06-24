import asyncio
import websockets
import time
import sys
import hashlib

# remember sockets or else they get trashed by the GC
receivers = []
senders = []

password = None

try:
    with open("password.cfg", "r") as f:
        password = f.read()
except:
    sys.exit(0)

async def hello(websocket, path):
        print("waiting to receive clients")
        client_data = await websocket.recv()

        is_sender = False
        if(client_data == "CONNECT_RECEIVER"):
            receivers.append(websocket)

        elif(client_data.startswith("CONNECT_SENDER")):
            is_sender = True

            client_pass = hashlib.sha256(client_data.split("|")[1].encode("utf-8"))
            print(client_pass)
            while(client_pass != password):
                await websocket.send("DENIED")

                client_data = await websocket.recv()
                client_pass = hashlib.sha256(client_data.split("|")[1].encode("utf-8"))

            await websocket.send("SUCCESS")

            senders.append(websocket)
        try:
            while True:
                print("waiting to receive data...")
                client_data = await websocket.recv()
                print("received data : " + client_data)

                if(client_data.startswith("RECEIVER_OUTPUT|")):
                    await broadcast_senders(client_data[16:])
                    continue
                
                else:
                    await broadcast_receivers(client_data)

        except Exception as e:
            print(str(e))

        finally:
            if(is_sender):
                senders.remove(websocket)
            else:
                receivers.remove(websocket)


async def broadcast_receivers(data):
    for client in receivers:       
        await client.send(data)

async def broadcast_senders(data):
    for client in senders:       
        await client.send(data)
            
        

# ping_interval None -> disables timeout
# max_size=None -> disable frame size limit
start_server = websockets.serve(hello, '192.168.4.148', 8766, ping_interval=None,max_size=None)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
