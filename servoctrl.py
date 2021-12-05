class ServoCtrl:
    def __init__(self, servo, angle_diff):
        self.servo = servo
        self.angle_diff = angle_diff

    def left(self):
        self.servo.angle -= self.angle_diff

    def right(self):
        self.servo.angle += self.angle_diff