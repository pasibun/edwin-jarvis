import RPi.GPIO as GPIO

from Domain.Enum.button_type_enum import ButtonType
from Domain.Enum.control_buttons_enum import ControlButton
from Domain.Enum.position_enum import Position
from Domain.button import Button


class ControlBoardService(object):
    base_left = Button(26, ButtonType.CONTROL_BUTTON, Position.CONTROL_BOARD, ControlButton.BASE_LEFT)
    base_right = Button(19, ButtonType.CONTROL_BUTTON, Position.CONTROL_BOARD, ControlButton.BASE_RIGHT)

    first_axis_left = Button(13, ButtonType.CONTROL_BUTTON, Position.CONTROL_BOARD,
                             ControlButton.FIRST_AXIS_LEFT)
    first_axis_right = Button(6, ButtonType.CONTROL_BUTTON, Position.CONTROL_BOARD,
                              ControlButton.FIRST_AXIS_RIGHT)

    def __init__(self):
        print("init controlBoard service")

    def get_button_pressed(self):
        if GPIO.input(self.base_left.PIN):
            self.return_pressed_button(self.base_left)
        elif GPIO.input(self.base_right.PIN):
            self.return_pressed_button(self.base_right)
        elif GPIO.input(self.first_axis_left.PIN):
            self.return_pressed_button(self.first_axis_left)
        elif GPIO.input(self.first_axis_right.PIN):
            self.return_pressed_button(self.first_axis_right)
        else:
            return "", False

    def return_pressed_button(self, btn):
        print(btn.CONTROL, " has been pressed")
        return btn.CONTROL, True
