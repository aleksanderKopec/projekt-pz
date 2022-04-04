import asyncio
import json
import websockets
clients = []

async def echo(websocket, server):
    print(f"Client added: {websocket}")
    clients.append(websocket)
    async for message in websocket:
        print(f"Got message: {json.loads(message)}")
        for client in clients:
            await client.send(message)

async def main():
    async with websockets.serve(echo, "localhost", 8765) as server:
        await asyncio.Future()

asyncio.run(main())