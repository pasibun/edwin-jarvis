import logging

import RPi.GPIO as GPIO
from time import sleep
from Domain.Enum.control_buttons_enum import ControlButton
from Service.mcp_driver_service import IOExpander
from Service.movement_service import MovementService
from Service.mqtt_service import MqttService


class EdwinJarvis(object):
    # control_board_service = ControlBoardService()
    stepper_motor = MovementService()
    io_expander = IOExpander()

    steps = 1
    speed = 0.001
    first_time = True

    def starting_control_board(self, mqtt_payload):
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


edwin = EdwinJarvis()


def clean_up():
    print("Exiting program.")
    GPIO.output(14, GPIO.LOW)
    GPIO.output(15, GPIO.LOW)


def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    value = ControlButton.FIRST_AXIS_LEFT
    if str(message.payload.decode("utf-8")).lower() == "right":
        value = ControlButton.BASE_RIGHT
    elif str(message.payload.decode("utf-8")).lower() == "left":
        value = ControlButton.BASE_LEFT
    elif str(message.payload.decode("utf-8")).lower() == "up":
        value = ControlButton.FIRST_AXIS_LEFT
    elif str(message.payload.decode("utf-8")).lower() == "down":
        value = ControlButton.FIRST_AXIS_RIGHT
    edwin.starting_control_board(value)


if __name__ == "__main__":
    try:
        logging.basicConfig(filename='logging.log', level=logging.INFO, format='%(asctime)s %(message)s')
        logging.info("Starting application. Saving logs in ~/logging.log")
        # GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        edwin.first_time_run()
        sleep(2)
        MqttService()
        clean_up()
    except KeyboardInterrupt:
        clean_up()
