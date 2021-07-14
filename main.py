"""
Version 0.1 of the IoT-based Security system
@author Usiwoma Oghenovo
"""
import sys
import livestream
import asyncio
from gpiozero import AngularServo, MotionSensor
import websockets

SERVO_PIN = 17
MOTION_PIN = 4
PORT = 8765


def connectToServer(url, motion_sensor, servo):
    servo_angle_diff = 45;

    async def connect():
        while True:
            try:
                print('Attempting to connect with server')
                async with websockets.connect(url) as websocket:
                    await websocket.send("LOG {}".format(PORT))
                    print('Device Logged')

                    async for message in websocket:
                        # Handle incoming messages
                        print("Received: " + message)
                        if (message.startswith('CAMERA')):
                            tokens = message.split("_")
                            direction = tokens[1]

                            if (direction == 'LEFT'):
                                servo.angle -= servo_angle_diff;
                            elif (direction == 'RIGHT'):
                                servo.angle += servo_angle_diff;

            except Exception as e:
                print('Error: ' + str(e))

    return connect


def main():
    #ip_address = sys.argv[1]
    server_url = sys.argv[1]

    servo = AngularServo(SERVO_PIN, min_angle=-90, max_angle=90)
    motion_sensor = MotionSensor(MOTION_PIN)

    livestream.start(PORT)
    asyncio.get_event_loop().run_in_executor(
        connectToServer(server_url, motion_sensor, servo))


if __name__ == "__main__":
    main()
