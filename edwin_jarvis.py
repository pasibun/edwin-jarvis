import RPi.GPIO as GPIO

from Domain.control_buttons import ControlButton
from Service.control_board_service import ControlBoardService
from Service.movement_service import MovementService
import logging


def starting_control_board():
    global motor
    stepper_motor = MovementService()
    control_board_service = ControlBoardService()
    steps = 1
    speed = 0.001
    direction = 1
    while True:
        result = control_board_service.what_button_is_pressed()
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
            stepper_motor.moving_to_new_step(motor, steps, direction, speed)


def clean_up():
    print("Exiting program.")
    GPIO.output(14, GPIO.LOW)
    GPIO.output(15, GPIO.LOW)
    GPIO.cleanup()


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
