import time

class ServoCtrl:
    def __init__(self, servo):
        self.servo = servo
        self.save_path = "/home/pi/servo.dat"
        self.current_position = ''
        with open(self.save_path, 'r') as file:
            self.current_position = file.readline()
        print(self.current_position)

    def left(self):
        if (self.current_position == 'left'):
            return
        self.rotate(0.1)
        self.set_current_position('left')

    def right(self):
        if (self.current_position == 'right'):
            return
        self.rotate(0.2)
        self.set_current_position('right')

    def rotate(self, cycle):
        # actual_cycle = 0.1 + (((cycle - (-1)) / (1 - (-1))) * (0.2 - 0.1))
        self.servo.value = cycle
        time.sleep(0.3)
        self.servo.value = 0

    def set_current_position(self, position):
        with open(self.save_path, 'w') as file:
            file.write(position + '\r')
            file.flush()
