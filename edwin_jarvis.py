import RPi.GPIO as GPIO
from Domain.Enum.control_buttons_enum import ControlButton
from Service.control_board_service import ControlBoardService
from Service.mcp_driver_service import IOExpander
from Service.movement_service import MovementService
import logging

from Service.mqtt_service import MqttService


class EdwinJarvis(object):
    control_board_service = ControlBoardService()
    stepper_motor = MovementService()
    io_expander = IOExpander()
    mqtt = MqttService()

    steps = 1
    speed = 0.001
    first_time = True

    def starting_control_board(self):
        motor = self.stepper_motor.stepper_motor_first_axis
        direction = motor.CCW
        while True:
            result = self.control_board_service.get_button_pressed()
            if self.first_time:
                self.first_time_run()
            if result[0] == ControlButton.FIRST_AXIS_LEFT:
                motor = self.stepper_motor.stepper_motor_first_axis
                direction = motor.CCW
            elif result[0] == ControlButton.FIRST_AXIS_RIGHT:
                motor = self.stepper_motor.stepper_motor_first_axis
                direction = motor.CW
            elif result[0] == ControlButton.BASE_LEFT:
                motor = self.stepper_motor.stepper_motor_base
                direction = motor.CCW
            elif result[0] == ControlButton.BASE_RIGHT:
                motor = self.stepper_motor.stepper_motor_base
                direction = motor.CW
            if result[1]:
                self.run_motor_with_led(motor, direction)

    def run_motor_with_led(self, motor, direction):
        self.io_expander.write_digital(self.io_expander.led_pin, 1)
        if motor.stop_switch_left is not None:
            stop_switch_left = motor.stop_switch_left.PIN
            stop_switch_right = motor.stop_switch_right.PIN
        else:
            stop_switch_left = ''
            stop_switch_right = ''
        self.stepper_motor.moving_to_new_step(motor, self.steps, direction, self.speed, stop_switch_left,
                                              stop_switch_right)
        self.io_expander.write_digital(self.io_expander.led_pin, 0)

    def first_time_run(self):
        self.io_expander.write_digital(self.io_expander.led_pin, 1)
        motor = self.stepper_motor.stepper_motor_first_axis
        stop_switch_left = motor.stop_switch_left.PIN
        stop_switch_right = motor.stop_switch_right.PIN

        self.stepper_motor.moving_to_new_step(motor, 500, motor.CCW, self.speed, stop_switch_left,
                                              stop_switch_right)
        self.first_time = False
        self.io_expander.write_digital(self.io_expander.led_pin, 0)

    def clean_up(self):
        print("Exiting program.")
        GPIO.output(14, GPIO.LOW)
        GPIO.output(15, GPIO.LOW)


edwin = EdwinJarvis()
if __name__ == "__main__":
    try:
        logging.basicConfig(filename='logging.log', level=logging.INFO, format='%(asctime)s %(message)s')
        logging.info("Starting application. Saving logs in ~/logging.log")
        # GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        edwin.starting_control_board()
        edwin.clean_up()
    except KeyboardInterrupt:
        edwin.clean_up()
