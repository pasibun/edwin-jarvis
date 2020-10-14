import logging

import RPi.GPIO as GPIO
from time import sleep
from Domain.Enum.control_buttons_enum import ControlButton
from Service.mcp_driver_service import IOExpander
from Service.movement_service import MovementService
from Service.mqtt_service import MqttService


class EdwinJarvis(object):
    stepper_motor = MovementService()
    io_expander = IOExpander()

    def first_time_run(self):
        self.io_expander.write_digital(self.io_expander.led_pin, 1)
        motor = self.stepper_motor.stepper_motor_first_axis
        stop_switch_left = motor.stop_switch_left.PIN
        stop_switch_right = motor.stop_switch_right.PIN

        self.stepper_motor.moving_to_new_step(motor, 500, motor.CCW, 0.001, stop_switch_left,
                                              stop_switch_right)
        self.io_expander.write_digital(self.io_expander.led_pin, 0)


edwin = EdwinJarvis()


def clean_up():
    print("Exiting program.")
    GPIO.output(14, GPIO.LOW)
    GPIO.output(15, GPIO.LOW)


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
