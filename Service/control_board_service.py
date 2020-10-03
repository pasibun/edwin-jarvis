from Domain.button import Button
import RPi.GPIO as GPIO


class ControlBoardService(object):
    base_left = Button(37, 'baseLeft')  # GPIO26
    base_right = Button(35, 'baseRight')  # GPIO19
    first_axis_left = Button(33, 'firstAxisLeft')  # GPIO13
    first_axis_right = Button(31, 'firstAxisRight')  # GPIO6

    def __init__(self):
        print("init controlBoard service")
        self.init_base_stop_btn()

    def init_base_stop_btn(self):
        GPIO.setup(self.base_left.PIN, GPIO.IN)
        GPIO.setup(self.base_right.PIN, GPIO.IN)
        GPIO.setup(self.first_axis_left.PIN, GPIO.IN)
        GPIO.setup(self.first_axis_right.PIN, GPIO.IN)

    def what_button_is_pressed(self):
        if GPIO.input(self.base_left.PIN):
            print("Base left has been pressed")
            return self.base_left, True
        # if GPIO.input(self.base_right.PIN):
        #     print("Base right has been pressed")
        #     return self.base_right, True
        # if GPIO.input(self.first_axis_left.PIN):
        #     print("First axis left has been pressed")
        #     return self.first_axis_left, True
        # if GPIO.input(self.first_axis_right.PIN):
        #     print("First axis right has been pressed")
        #     return self.first_axis_right, True

