"""
Version 0.1 of the IoT-based Security system
@author Usiwoma Oghenovo
"""
import sys
import livestream
import web_logging
import asyncio
import threading
import time
import picamera
from gpiozero import AngularServo, MotionSensor
import websockets

SERVO_PIN = 17
MOTION_PIN = 4
PORT = 8080
CAPTURE_DIR = "/home/pi/captures/"

camera = picamera.PiCamera(resolution=(480, 360))
message_queue = asyncio.Queue()


async def listenToServer(url, servo, logger):
    servo_angle_diff = 45

    while True:
        try:
            print('Attempting to connect with server')
            async with websockets.connect(url) as websocket:
                message_queue.put_nowait("LOG {}".format(PORT))

                async for message in websocket:
                    # Handle incoming messages
                    print("Received: " + message)
                    if (message.startswith('CAMERA')):
                        tokens = message.split("_")
                        direction = tokens[1]

                        if (direction == 'LEFT'):
                            servo.angle -= servo_angle_diff
                        elif (direction == 'RIGHT'):
                            servo.angle += servo_angle_diff
                    elif (message == "CAPTURE"):
                        capture()

        except Exception as e:
            print('Error: ' + str(e))
            logger.log(str(e))


async def sendFromQueue(url, logger):
    while True:
        try:
            async with websockets.connect(url) as websocket:
                message = await message_queue.get()
                await websocket.send(message)
        except Exception as e:
            logger.log(str(e))


def listenForMotion():
    motion_sensor = MotionSensor(MOTION_PIN)

    def onMotion():
        try:
            message_queue.put_nowait("MOTION")
            capture()
        except Exception as e:
            print("Couldn't handle motion: " + str(e))

    motion_sensor.when_motion = onMotion
    motion_sensor.when_no_motion = onMotion
    # logger.log("Motion sensor is configured")


def capture():
    camera.capture(CAPTURE_DIR + 'Capture_' + str(time.time()) + '.jpg')


def main():
    server_url = sys.argv[1]
    log_url = sys.argv[2]
    logger = web_logging.Logger(log_url)

    try:
        logger.log("[+] Device ON")
        servo = AngularServo(SERVO_PIN, min_angle=-90, max_angle=90)

        # camera.vflip = True
        # Start a preview and let the camera warm up for 2 seconds
        camera.start_preview()
        time.sleep(2)
        camera.stop_preview()

        threading.Thread(target=listenForMotion, daemon=True).start()

        asyncio.ensure_future(
            listenToServer(server_url, servo, logger))
        asyncio.ensure_future(
            sendFromQueue(server_url, logger))
        asyncio.ensure_future(livestream.start(server_url, camera, logger))
        asyncio.get_event_loop().run_forever()
    except Exception as e:
        logger.log(str(e))


if __name__ == "__main__":
    main()
