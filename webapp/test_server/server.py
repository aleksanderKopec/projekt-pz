import asyncio
import json
import websockets
clients = []

async def echo(websocket, server):
    print(f"Client added: {websocket}")
    clients.append(websocket)
    async for message in websocket:
        print(f"Got message: {message}")
        for client in clients:
            msg = {"author": "Alek", "message": message}
            await client.send(json.dumps(msg))

async def main():
    async with websockets.serve(echo, "localhost", 3100) as server:
        await asyncio.Future()

asyncio.run(main())