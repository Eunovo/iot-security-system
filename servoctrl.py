import time
from threading import Thread
from queue import Empty, Queue


class ServoCtrl(Thread):
    def __init__(self, servo):
        super().__init__()
        self.queue = Queue()
        self.lefts = 0
        self.rights = 0
        self.servo = servo
        self.save_path = "/home/pi/servo.dat"
        self.current_position = ''
        with open(self.save_path, 'r') as file:
            self.current_position = file.read()
        print('Current Position: ', self.current_position)

    def run(self):
        while True:
            try:
                if (self.lefts == self.rights):
                    continue

                new_position = 'left'
                self.lefts -= 1
                if (self.rights > self.lefts):
                    new_position = 'right'
                    self.rights -= 1
                    self.lefts += 1
                
                if (self.current_position == new_position):
                    continue

                self.rotate({
                    'left': 0.1, 'right': 0.2
                }.get(new_position))
                self.set_current_position(new_position)
                
                # pause
                time.sleep(5)
            except Empty:
                pass

    def left(self):
        # self.queue.put_nowait('left')
        self.lefts += 1

    def right(self):
        # self.queue.put_nowait('right')
        self.rights += 1

    def rotate(self, cycle):
        # actual_cycle = 0.1 + (((cycle - (-1)) / (1 - (-1))) * (0.2 - 0.1))
        self.servo.value = cycle
        time.sleep(0.5)
        self.servo.value = 0

    def set_current_position(self, position):
        self.current_position = position
        print('Current Position: ', position)
        with open(self.save_path, 'w') as file:
            file.write(position)
            file.flush()
