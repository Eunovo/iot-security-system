import time

class ServoCtrl:
    def __init__(self, servo):
        self.servo = servo
        initial_angle = 0
        self.current_angle = initial_angle

    def left(self):
        self.rotate(0.1)

    def right(self):
        self.rotate(0.2)

    def rotate(self, cycle):
        # actual_cycle = 0.1 + (((cycle - (-1)) / (1 - (-1))) * (0.2 - 0.1))
        self.servo.value = cycle
        time.sleep(0.3)
        self.servo.value = 0
