"""
Version 0.1 of the IoT-based Security system
@author Usiwoma Oghenovo
"""
import sys
import livestream
import asyncio
import websockets

PORT = 8765

async def connectToServer(url):
    async with websockets.connect(url) as websocket:
        await websocket.send("LOG {}".format(PORT))


def main():
    #ip_address = sys.argv[1]
    server_url = sys.argv[1]

    asyncio.get_event_loop().run_until_complete(connectToServer(server_url))
    livestream.start(PORT)


if __name__ == "__main__":
    main()
