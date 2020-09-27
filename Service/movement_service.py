import RPi.GPIO as GPIO
from time import sleep
from Domain.stepper_motor import StepperMotor
from Domain.stop_switch import StopSwitchButton


# MODE = (14, 15, 18) # Microstep Resolution GPIO Pins
# GPIO.setup(MODE, GPIO.OUT)
# RESOLUTION = {'Full': (0, 0, 0),
#              'Half': (1, 0, 0),
#              '1/4': (0, 1, 0),
#              '1/8': (1, 1, 0),
#              '1/16': (0, 0, 1),
#              '1/32': (1, 0, 1)}
#
# GPIO.output(MODE, RESOLUTION['1/32'])


class MovementService(object):
    stepper_motor_base = StepperMotor(21, 20)

    base_stop_btn_left = StopSwitchButton(22, 'BaseStopLeft')
    base_stop_btn_right = StopSwitchButton(23, 'BaseStopRight')

    def __init__(self):
        self.init_stepper_motors()
        self.init_base_stop_btn()

    def init_stepper_motors(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.stepper_motor_base.DIR, GPIO.OUT)
        GPIO.setup(self.stepper_motor_base.STEP, GPIO.OUT)
        GPIO.output(self.stepper_motor_base.DIR, self.stepper_motor_base.CW)

    def init_base_stop_btn(self):
        GPIO.setup(self.base_stop_btn_left.PIN, GPIO.IN)
        GPIO.setup(self.base_stop_btn_right.PIN, GPIO.IN)

    def moving(self, steppermotor, steps, direction, speed):
        GPIO.output(steppermotor.DIR, direction)
        for x in range(steps):
            GPIO.output(steppermotor.STEP, GPIO.HIGH)
            sleep(speed)
            GPIO.output(steppermotor.STEP, GPIO.LOW)
            sleep(speed)
            if self.base_stop_switch_check():
                break

    def base_stop_switch_check(self):
        return GPIO.input(self.base_stop_btn_left.PIN) == 1 or GPIO.input(self.base_stop_btn_right.PIN) == 1
