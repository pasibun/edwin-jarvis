from Domain.Enum.button_type_enum import ButtonType
from Domain.Enum.position_enum import Position
from Domain.button import Button
import RPi.GPIO as GPIO

from Domain.control_buttons import ControlButton


class ControlBoardService(object):
    base_left = Button(26, ButtonType.CONTROL_BUTTON, Position.CONTROL_BOARD)  # GPIO26
    base_right = Button(19, ButtonType.CONTROL_BUTTON, Position.CONTROL_BOARD)  # GPIO19
    first_axis_left = Button(13, ButtonType.CONTROL_BUTTON, Position.CONTROL_BOARD)  # GPIO13
    first_axis_right = Button(6, ButtonType.CONTROL_BUTTON, Position.CONTROL_BOARD)  # GPIO6

    def __init__(self):
        print("init controlBoard service")

    def what_button_is_pressed(self):
        if GPIO.input(self.base_left.PIN):
            print("Base left has been pressed")
            return ControlButton.BASE_LEFT, True
        elif GPIO.input(self.base_right.PIN):
            print("Base right has been pressed")
            return ControlButton.BASE_RIGHT, True
        elif GPIO.input(self.first_axis_left.PIN):
            print("First axis left has been pressed")
            return ControlButton.FIRST_AXIS_LEFT, True
        elif GPIO.input(self.first_axis_right.PIN):
            print("First axis right has been pressed")
            return ControlButton.FIRST_AXIS_RIGHT, True
        else:
            return "", False
