from Service.control_board_service import ControlBoardService
from Service.movement_service import MovementService
import logging


def m():
    steppermotor = MovementService()
    # motor = steppermotor.stepper_motor_base
    # steps = motor.SPR * 4
    # direction = motor.CW
    # delay = .005 / 32
    # steppermotor.moving(motor.DIR, motor.STEP, steps, direction, delay)
    steppermotor.base_stop_switch_check()


def n():
    controlBoardService = ControlBoardService()


if __name__ == "__main__":
    try:
        logging.basicConfig(filename='logging.log', level=logging.INFO, format='%(asctime)s %(message)s')
        logging.info("Starting application. Saving logs in ~/logging.log")
        m()
    except KeyboardInterrupt:
        print("Exiting program.")
