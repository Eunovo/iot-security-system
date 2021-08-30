"""
Version 0.1 of the IoT-based Security system
@author Usiwoma Oghenovo
"""
import sys
import livestream
import web_logging
import asyncio
import time
import picamera
from gpiozero import AngularServo, MotionSensor
import websockets

SERVO_PIN = 17
MOTION_PIN = 4
PORT = 8080


async def connectToServer(url, motion_sensor, servo, camera, logger):
    servo_angle_diff = 45

    def capture():
        camera.capture('Capture_' + str(time.time()))

    while True:
        try:
            print('Attempting to connect with server')
            async with websockets.connect(url) as websocket:
                await websocket.send("LOG {}".format(PORT))
                print('Device Logged')

                def onMotion(websocket):
                    try:
                        websocket.send("MOTION")
                        capture()
                    except Exception as e:
                        print("Couldn't handle motion: " + str(e))

                motion_sensor.when_motion = onMotion
                motion_sensor.when_no_motion = onMotion

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


def main():
    #ip_address = sys.argv[1]
    server_url = sys.argv[1]
    log_url = sys.argv[2]
    logger = web_logging.Logger(log_url)

    try:
        logger.log("[+] Device ON")
        servo = AngularServo(SERVO_PIN, min_angle=-90, max_angle=90)
        motion_sensor = MotionSensor(MOTION_PIN)
        camera = picamera.PiCamera()
        # camera.vflip = True
        camera.resolution = (500, 480)
        # Start a preview and let the camera warm up for 2 seconds
        camera.start_preview()
        time.sleep(2)
        camera.stop_preview()

        asyncio.ensure_future(
            connectToServer(server_url, motion_sensor, servo, camera, logger))
        asyncio.ensure_future(livestream.start(PORT, camera))
        asyncio.get_event_loop().run_forever()
    except Exception as e:
        logger.log(str(e))


if __name__ == "__main__":
    main()
