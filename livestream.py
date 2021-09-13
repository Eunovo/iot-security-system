import websockets
import io
import struct
import time


async def startStream(url, camera, web_logger):
    while True:
        try:
            async with websockets.connect(url) as websocket:
                await websocket.send('STREAM')

                start = time.time()
                stream = io.BytesIO()
                for foo in camera.capture_continuous(stream, 'jpeg'):
                    # Write the length of the capture to the stream and flush to
                    # ensure it actually gets sent
                    await websocket.send(struct.pack('<L', stream.tell()))

                    # Rewind the stream and send the image data over the wire
                    stream.seek(0)
                    await websocket.send(stream.read())
                    # If we've been capturing for more than 30 seconds, quit
                    if time.time() - start > 60:
                        break
                    # Reset the stream for the next capture
                    stream.seek(0)
                    stream.truncate()
                # Write a length of zero to the stream to signal we're done
                websocket.send(struct.pack('<L', 0))
        except Exception as e:
            web_logger.log('[pi] Error occured: '+str(e))


async def start(server_url, camera, web_logger):
    web_logger.log("[pi] Starting Stream")
    await startStream(server_url, camera, web_logger)
    # await websockets.serve(serve(camera), "localhost", port)
