from time import sleep

import RPi.GPIO as GPIO

from Domain.button import Button
from Domain.stepper_motor import StepperMotor


class MovementService(object):
    stepper_motor_base = StepperMotor(36, 34)  # GPIO16/GPIO12
    stepper_motor_first_axis = StepperMotor(40, 38)  # GPIO21/GPIO20

    base_stop_btn_left = Button(23, 'BaseStopLeft')  # GPIO11
    base_stop_btn_right = Button(29, 'BaseStopRight')  # GPIO5

    def __init__(self):
        print("init movement service")
        self.init_stepper_motors()
        self.init_base_stop_btn()

    def init_stepper_motors(self):
        GPIO.setup(self.stepper_motor_first_axis.DIR, GPIO.OUT)
        GPIO.setup(self.stepper_motor_first_axis.STEP, GPIO.OUT)
        GPIO.setup(self.stepper_motor_base.DIR, GPIO.OUT)
        GPIO.setup(self.stepper_motor_base.STEP, GPIO.OUT)

    def init_base_stop_btn(self):
        GPIO.setup(self.base_stop_btn_left.PIN, GPIO.IN)
        GPIO.setup(self.base_stop_btn_right.PIN, GPIO.IN)

    def moving(self, motor, steps, direction, speed):
        dir_pin = motor.DIR
        step_pin = motor.STEP
        GPIO.output(dir_pin, direction)
        print('Moving to step: ', steps)
        for x in range(steps):
            motor.new_current_step(x)
            GPIO.output(step_pin, GPIO.HIGH)
            sleep(speed)
            GPIO.output(step_pin, GPIO.LOW)
            sleep(speed)
            if self.base_stop_switch_check():
                print("Stop switch has been pressed!")
                break

    def base_stop_switch_check(self):
        return GPIO.input(self.base_stop_btn_left.PIN) or GPIO.input(self.base_stop_btn_right.PIN)

    def reset_motor_positions(self):
        print("dingen")
