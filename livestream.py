import asyncio
import websockets
import io
import struct
import time
# import picamera


def serve(camera):
    def handleSocket(websocket, path):
        print("[+] Connection Established with... " + websocket.remote_address)

        try:
            # camera = picamera.PiCamera()
            # camera.vflip = True
            # camera.resolution = (500, 480)
            # # Start a preview and let the camera warm up for 2 seconds
            # camera.start_preview()
            # time.sleep(2)

            # Note the start time and construct a stream to hold image data
            # temporarily (we could write it directly to connection but in this
            # case we want to find out the size of each capture first to keep
            # our protocol simple)
            start = time.time()
            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg'):
                # Write the length of the capture to the stream and flush to
                # ensure it actually gets sent
                websocket.send(struct.pack('<L', stream.tell()))

                # Rewind the stream and send the image data over the wire
                stream.seek(0)
                websocket.send(stream.read())
                # If we've been capturing for more than 30 seconds, quit
                if time.time() - start > 60:
                    break
                # Reset the stream for the next capture
                stream.seek(0)
                stream.truncate()
            # Write a length of zero to the stream to signal we're done
            websocket.send(struct.pack('<L', 0))
        except Exception as e:
            print("[-] Error: " + str(e))
        finally:
            print("[-] Connection closed...")
            websocket.close()
    
    return handleSocket


async def start_server(port, camera): return websockets.serve(serve(camera), "localhost", port)


def start(port, camera):
    print("[+] Starting WebSocket Server")
    asyncio.get_event_loop().run_until_complete(start_server(port, camera))
    asyncio.get_event_loop().run_forever()
