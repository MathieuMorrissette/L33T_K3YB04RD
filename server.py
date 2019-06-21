import asyncio
import websockets


connected_clients = []

async def hello(websocket, path):
    while(True):
        print("waiting to receive clients")
        client_data = await websocket.recv()

        if(client_data == "CONNECT"):
            print("registered 1 client")
            connected_clients.append(websocket)
            print("total registered : " + str(len(connected_clients)))
        elif(client_data.startswith("KEY|")):
            await broadcast_key(client_data[4:])



async def broadcast_key(key):
    for client in connected_clients:            
        await client.send(key)
            
        


start_server = websockets.serve(hello, 'localhost', 8766)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
