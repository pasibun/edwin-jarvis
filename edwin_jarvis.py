from Service.movement_service import MovementService
import logging

if __name__ == "__main__":
    logging.basicConfig(filename='logging.log', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info("Starting application. Saving logs in ~/logging.log")

    steppermotor = MovementService()
    motor = steppermotor.stepper_motor_base
    steps = motor.SPR * 4
    direction = motor.CW
    delay = .005 / 32
    steppermotor.moving(300, steppermotor.stepper_motor_base, direction, delay)
