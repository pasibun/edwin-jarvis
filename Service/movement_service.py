from time import sleep
import RPi.GPIO as GPIO
from Domain.button import Button
from Domain.stepper_motor import StepperMotor


class MovementService(object):
    stepper_motor_base = StepperMotor(16, 12, [7, 8, 25], '1/4')
    stepper_motor_first_axis = StepperMotor(21, 20, [24, 23, 18], '1/4')

    base_stop_btn_left = Button(11, 'BaseStopLeft')
    base_stop_btn_right = Button(5, 'BaseStopRight')

    def __init__(self):
        print("init movement service")
        self.init_base_stop_btn()

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
