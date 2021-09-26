import websockets
import io, asyncio
import threading, queue

data_queue = queue.Queue()


def readImageStream(camera, web_logger):
    web_logger.log('Reading stream')
    stream = io.BytesIO()
    for foo in camera.capture_continuous(stream, 'jpeg'):
        # Rewind the stream and send the image data over the wire
        stream.seek(0)
        data = stream.read()
        print('i have '+ str(len(data)))
        data_queue.put_nowait(data)
        print('put '+ str(len(data)))
        # Reset the stream for the next capture
        stream.seek(0)
        stream.truncate()


async def startStream(url, web_logger):
    while True:
        try:
            async with websockets.connect(url) as websocket:
                await websocket.send('STREAM')
                print("'STREAM' sent")

                while True:
                    data = data_queue.get()
                    await websocket.send(data)
                    print("Sent: ", str(len(data)), " bytes")
        except Exception as e:
            error_msg = '[pi] Error occured: '+str(e)
            web_logger.log(error_msg)


async def start(server_url, camera, web_logger):
    web_logger.log("[pi] Starting Stream...")
    def reader():
        readImageStream(camera, web_logger)
    def streamer():
        asyncio.run(startStream(server_url, web_logger))

    threading.Thread(target=reader, daemon=True).start()
    threading.Thread(target=streamer, daemon=True).start()
    threading.Thread(target=streamer, daemon=True).start()
    threading.Thread(target=streamer, daemon=True).start()
