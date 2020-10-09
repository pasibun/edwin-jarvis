import RPi.GPIO as GPIO
from Domain.control_buttons import ControlButton
from Service.control_board_service import ControlBoardService
from Service.mcp_driver_service import IOExpander
from Service.movement_service import MovementService
import logging


def starting_control_board():
    global motor
    control_board_service = ControlBoardService()
    stepper_motor = MovementService()
    io_expander = IOExpander()
    steps = 1
    speed = 0.001
    direction = 1
    first_time = True
    while True:
        result = control_board_service.what_button_is_pressed()
        if first_time:
            io_expander.write_digital(io_expander.led_pin, 1)
            motor = stepper_motor.stepper_motor_first_axis
            direction = motor.CCW
            stepper_motor.moving_to_new_step(motor, 500, direction, speed)
            first_time = False
            io_expander.write_digital(io_expander.led_pin, 0)
        if result[0] == ControlButton.FIRST_AXIS_LEFT:
            motor = stepper_motor.stepper_motor_first_axis
            direction = motor.CCW
        elif result[0] == ControlButton.FIRST_AXIS_RIGHT:
            motor = stepper_motor.stepper_motor_first_axis
            direction = motor.CW
        elif result[0] == ControlButton.BASE_LEFT:
            motor = stepper_motor.stepper_motor_base
            direction = motor.CCW
        elif result[0] == ControlButton.BASE_RIGHT:
            motor = stepper_motor.stepper_motor_base
            direction = motor.CW
        if result[1]:
            io_expander.write_digital(io_expander.led_pin, 1)
            stepper_motor.moving_to_new_step(motor, steps, direction, speed)
            io_expander.write_digital(io_expander.led_pin, 0)


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
        starting_control_board()
        clean_up()
    except KeyboardInterrupt:
        clean_up()
