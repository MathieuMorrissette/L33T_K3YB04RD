import asyncio
import websockets
import time
# remember sockets or else they get trashed by the GC
receivers = []
senders = []

async def hello(websocket, path):
        print("waiting to receive clients")
        client_data = await websocket.recv()

        is_sender = False
        if(client_data == "CONNECT_RECEIVER"):
            receivers.append(websocket)

        elif(client_data == "CONNECT_SENDER"):
            is_sender = True
            senders.append(websocket)
        try:
            while True:
                print("waiting to receive data...")
                client_data = await websocket.recv()
                print("received data : " + client_data)

                if(client_data.startswith("KEY|")):
                    key = client_data[4:]
                    print("sending " + key)
                    await broadcast_key(key)
                    print("done sending")

        except Exception as e:
            print(str(e))

        finally:
            if(is_sender):
                senders.remove(websocket)
            else:
                receivers.remove(websocket)


async def broadcast_key(key):
    for client in receivers:       
        await client.send(key)
            
        

# ping_interval None -> disables timeout
start_server = websockets.serve(hello, '192.168.4.148', 8766, ping_interval=None)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
