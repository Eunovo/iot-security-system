import websockets
import io
import struct


async def startStream(url, camera, web_logger):
    while True:
        try:
            async with websockets.connect(url) as websocket:
                await websocket.send('STREAM')

                stream = io.BytesIO()
                for foo in camera.capture_continuous(stream, 'jpeg'):
                    # Write the length of the capture to the stream and flush to
                    # ensure it actually gets sent
                    print("Sent: ", stream.tell(), " bytes")

                    # Rewind the stream and send the image data over the wire
                    stream.seek(0)
                    data = stream.read()
                    # print(data)
                    await websocket.send(data)
                    # Reset the stream for the next capture
                    stream.seek(0)
                    stream.truncate()

                # Write a length of zero to the stream to signal we're done
                websocket.send(struct.pack('<L', 0))
        except Exception as e:
            error_msg = '[pi] Error occured: '+str(e)
            print(error_msg)
            web_logger.log(error_msg)


async def start(server_url, camera, web_logger):
    web_logger.log("[pi] Starting Stream...")
    await startStream(server_url, camera, web_logger)
    # await websockets.serve(serve(camera), "localhost", port)
