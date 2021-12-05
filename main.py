"""
Version 0.1 of the IoT-based Security system
@author Usiwoma Oghenovo
"""
import sys
import cameractrl
import servoctrl
import livestream
import web_logging
import asyncio
import threading
import time
import picamera
from gpiozero import AngularServo, DigitalInputDevice, MotionSensor
import websockets

SERVO_PIN = 17
MOTION_PIN = 4
MIC_LEFT_PIN = 22
MIC_RIGHT_PIN = 23
PORT = 8080
CAPTURE_DIR = "/home/pi/captures/"

camera = picamera.PiCamera(resolution=(480, 360))
cameraCtrl = cameractrl.CameraCtrl(camera, CAPTURE_DIR)
# servo = AngularServo(SERVO_PIN, min_angle=-90, max_angle=90)
# servoCtrl = servoctrl.ServoCtrl(servo, 45)
leftMic = DigitalInputDevice(MIC_LEFT_PIN)
rightMic = DigitalInputDevice(MIC_RIGHT_PIN)
message_queue = asyncio.Queue()


async def listenToServer(url, logger):
    while True:
        try:
            print('Attempting to connect with server')
            async with websockets.connect(url) as websocket:
                message_queue.put_nowait("LOG {}".format(PORT))
                async for message in websocket:
                    # Handle incoming messages
                    print("Received: " + message)
                    tokens = message.split("_")

                    try:
                        if (tokens[0] == 'CAMERA'):
                            direction = tokens[1]

                            # if (direction == 'LEFT'):
                            #     servoCtrl.left()
                            # elif (direction == 'RIGHT'):
                            #     servoCtrl.right()

                        elif (tokens[0] == "CAPTURE"):
                            cameraCtrl.capture()
                        elif (tokens[0] == "LIST"):
                            await message_queue.put(cameraCtrl.listImages())
                        elif (tokens[0] == 'READ'):
                            await message_queue.put(cameraCtrl.readImage(tokens[1]))
                    except e:
                        message_queue.put(str(e))
                        logger.log(str(e))

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


def listenForMotion(logger):
    motion_sensor = MotionSensor(MOTION_PIN)

    def onMotion():
        try:
            print("MOTION")
            message_queue.put_nowait("MOTION")
            cameraCtrl.capture()
        except Exception as e:
            logger("Couldn't handle motion: " + str(e))

    motion_sensor.when_motion = onMotion
    motion_sensor.when_no_motion = onMotion
    logger.log("Motion sensor is configured")


def main():
    server_url = sys.argv[1]
    log_url = sys.argv[2]
    logger = web_logging.Logger(log_url)

    try:
        logger.log("[+] Device ON")
        logSound = lambda x: lambda: logger.log("[+] Sound to the " + str(x))
        leftMic.when_activated = logSound('left with intensity: '+ str(leftMic.value))
        rightMic.when_activated = logSound('right with intensity: '+ str(rightMic.value))

        # servoCtrl.left()
        # time.sleep(2)
        # servoCtrl.right()
        # time.sleep(2)

        # camera.vflip = True
        # Start a preview and let the camera warm up for 2 seconds
        camera.start_preview()
        time.sleep(2)
        camera.stop_preview()
        # listenForMotion(logger)
        threading.Thread(target=listenForMotion, args=(
                         logger,), daemon=True).start()

        asyncio.ensure_future(
            listenToServer(server_url, logger))
        asyncio.ensure_future(
            sendFromQueue(server_url, logger))
        asyncio.ensure_future(livestream.start(server_url, camera, logger))
        asyncio.get_event_loop().run_forever()
    except Exception as e:
        logger.log(str(e))


if __name__ == "__main__":
    main()
