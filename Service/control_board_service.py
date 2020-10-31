from Domain.Enum.control_buttons_enum import ControlButton
from Service.movement_service import MovementService
from time import sleep


class ControlBoardService(object):
    stepper_motor = MovementService()

    speed = 0.001
    first_time = True

    def __init__(self):
        print("init controlBoard service")

    def first_time_run(self):
        motor = self.stepper_motor.stepper_motor_first_axis
        stop_switch_left = motor.stop_switch_left.PIN
        stop_switch_right = motor.stop_switch_right.PIN
        sleep(2)
        self.stepper_motor.active = True
        self.stepper_motor.start_process_moving(motor, motor.CCW, self.speed, stop_switch_left, stop_switch_right)

    def determine_motor_to_control(self, mqtt_payload):
        motor = self.stepper_motor.stepper_motor_first_axis
        direction = motor.CCW
        if mqtt_payload == ControlButton.FIRST_AXIS_LEFT:
            motor = self.stepper_motor.stepper_motor_first_axis
            direction = motor.CCW
        elif mqtt_payload == ControlButton.FIRST_AXIS_RIGHT:
            motor = self.stepper_motor.stepper_motor_first_axis
            direction = motor.CW
        elif mqtt_payload == ControlButton.BASE_LEFT:
            motor = self.stepper_motor.stepper_motor_base
            direction = motor.CCW
        elif mqtt_payload == ControlButton.BASE_RIGHT:
            motor = self.stepper_motor.stepper_motor_base
            direction = motor.CW
        self.run_motor_with_led(motor, direction)

    def run_motor_with_led(self, motor, direction):
        self.stepper_motor.active = True
        if motor.stop_switch_left is not None:
            stop_switch_left = motor.stop_switch_left.PIN
            stop_switch_right = motor.stop_switch_right.PIN
        else:
            stop_switch_left = ''
            stop_switch_right = ''
        self.stepper_motor.start_process_moving(motor, direction, self.speed, stop_switch_left, stop_switch_right)

    # base_left = Button(26, ButtonType.CONTROL_BUTTON, Position.CONTROL_BOARD, ControlButton.BASE_LEFT)
    # base_right = Button(19, ButtonType.CONTROL_BUTTON, Position.CONTROL_BOARD, ControlButton.BASE_RIGHT)
    #
    # first_axis_left = Button(13, ButtonType.CONTROL_BUTTON, Position.CONTROL_BOARD,
    #                          ControlButton.FIRST_AXIS_LEFT)
    # first_axis_right = Button(6, ButtonType.CONTROL_BUTTON, Position.CONTROL_BOARD,
    #                           ControlButton.FIRST_AXIS_RIGHT)

    # def get_button_pressed(self):
    #     if GPIO.input(self.base_left.PIN):
    #         return self.base_left.CONTROL, True
    #     elif GPIO.input(self.base_right.PIN):
    #         return self.base_right.CONTROL, True
    #     elif GPIO.input(self.first_axis_left.PIN):
    #         return self.first_axis_left.CONTROL, True
    #     elif GPIO.input(self.first_axis_right.PIN):
    #         return self.first_axis_right.CONTROL, True
    #     else:
    #         return "", False
