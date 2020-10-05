import RPi.GPIO as GPIO

from Domain.control_buttons import ControlButton
from Service.control_board_service import ControlBoardService
from Service.movement_service import MovementService
import logging


def starting_control_board():
    global motor
    control_board_service = ControlBoardService()
    stepper_motor = MovementService()
    steps = 500
    speed = 0.1
    direction = 1
    while True:
        result = control_board_service.what_button_is_pressed()
        if list(result.keys())[0] == ControlButton.FIRST_AXIS_LEFT:
            motor = stepper_motor.stepper_motor_first_axis
            direction = motor.CCW
        if list(result.keys())[0] == ControlButton.FIRST_AXIS_RIGHT:
            motor = stepper_motor.stepper_motor_first_axis
            direction = motor.CW
        if list(result.keys())[0] == ControlButton.BASE_LEFT:
            motor = stepper_motor.stepper_motor_base
            direction = motor.CCW
        if list(result.keys())[0] == ControlButton.BASE_RIGHT:
            motor = stepper_motor.stepper_motor_base
            direction = motor.CW
        stepper_motor.moving(motor.DIR, motor.STEP, steps, direction, speed)


def clean_up():
    print("Exiting program.")
    GPIO.cleanup()


if __name__ == "__main__":
    try:
        logging.basicConfig(filename='logging.log', level=logging.INFO, format='%(asctime)s %(message)s')
        logging.info("Starting application. Saving logs in ~/logging.log")
        GPIO.setmode(GPIO.BOARD)
        # GPIO.setwarnings(False)
        starting_control_board()
        clean_up()
    except KeyboardInterrupt:
        clean_up()
