import RPi.GPIO as GPIO
from time import sleep
from Domain.stepper_motor import StepperMotor
from Domain.button import Button


class MovementService(object):
    stepper_motor_base = StepperMotor(40, 38)  # GPIO21/GPIO20

    base_stop_btn_left = Button(23, 'BaseStopLeft')  # GPIO11
    base_stop_btn_right = Button(29, 'BaseStopRight')  # GPIO5

    def __init__(self):
        print("init movementService")
        self.init_stepper_motors()
        self.init_base_stop_btn()

    def init_stepper_motors(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.stepper_motor_base.DIR, GPIO.OUT)
        GPIO.setup(self.stepper_motor_base.STEP, GPIO.OUT)
        GPIO.output(self.stepper_motor_base.DIR, self.stepper_motor_base.CW)

    def init_base_stop_btn(self):
        GPIO.setup(self.base_stop_btn_left.PIN, GPIO.IN)
        GPIO.setup(self.base_stop_btn_right.PIN, GPIO.IN)

    def moving(self, dir_pin, step_pin, steps, direction, speed):
        GPIO.output(dir_pin, direction)
        for x in range(steps):
            GPIO.output(step_pin, GPIO.HIGH)
            sleep(speed)
            GPIO.output(step_pin, GPIO.LOW)
            sleep(speed)
            if self.base_stop_switch_check():
                break

    def base_stop_switch_check(self):
        return GPIO.input(self.base_stop_btn_left.PIN) == 1 or GPIO.input(self.base_stop_btn_right.PIN) == 1
