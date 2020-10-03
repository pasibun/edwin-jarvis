import RPi.GPIO as GPIO
from Service.control_board_service import ControlBoardService
from Service.movement_service import MovementService
import logging


def m():
    steppermotor = MovementService()
    motor = steppermotor.stepper_motor_first_axis
    steps = 500
    direction = motor.CW
    speed = 0.1
    steppermotor.moving(motor.DIR, motor.STEP, steps, direction, speed)


def n():
    controlboardservice = ControlBoardService()
    while True:
        controlboardservice.what_button_is_pressed()

def clean_up():
    print("Exiting program.")
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        logging.basicConfig(filename='logging.log', level=logging.INFO, format='%(asctime)s %(message)s')
        logging.info("Starting application. Saving logs in ~/logging.log")
        GPIO.setmode(GPIO.BOARD)
        # GPIO.setwarnings(False)
        m()
        clean_up()
    except KeyboardInterrupt:
        clean_up()
