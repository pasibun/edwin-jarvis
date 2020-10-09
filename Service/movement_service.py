from time import sleep
import RPi.GPIO as GPIO
from Domain.button import Button
from Domain.Enum.button_type_enum import ButtonType
from Domain.Enum.position_enum import Position
from Domain.stepper_motor import StepperMotor


class MovementService(object):
    default_speed = 0.001
    stepper_motor_base = StepperMotor(16, 12, 15, (7, 8, 25), '1/4')
    stepper_motor_first_axis = StepperMotor(21, 20, 14, (24, 23, 18), '1/4')

    first_axis_stop_switch_left = Button(11, ButtonType.STOPS_WITCH, Position.FIRST_AXIS_LEFT)
    first_axis_stop_switch_right = Button(5, ButtonType.STOPS_WITCH, Position.FIRST_AXIS_RIGHT)

    def __init__(self):
        print("init movement service")
        GPIO.output(self.stepper_motor_base.SLEEP, GPIO.HIGH)
        GPIO.output(self.stepper_motor_first_axis.SLEEP, GPIO.HIGH)

    def moving_to_new_step(self, motor, steps, direction, speed):
        dir_pin = motor.DIR
        step_pin = motor.STEP
        GPIO.output(dir_pin, direction)
        GPIO.output(motor.SLEEP, GPIO.HIGH)
        for x in range(steps):
            motor.new_current_step(x+1, direction)
            GPIO.output(step_pin, GPIO.HIGH)
            sleep(speed)
            GPIO.output(step_pin, GPIO.LOW)
            sleep(speed)
            if self.first_axis_stop_switch_check(motor):
                GPIO.output(motor.SLEEP, GPIO.LOW)
                sleep(1)
                break
        print("New motor step position: ", motor.current_step)

    def first_axis_stop_switch_check(self, motor):
        if GPIO.input(self.first_axis_stop_switch_left.PIN):
            print("Left stop switch has been pressed")
            self.move_motor(motor, motor.CCW)
            motor.current_step = 0
            return True
        elif GPIO.input(self.first_axis_stop_switch_right.PIN):
            print("Right stop switch has been pressed")
            self.move_motor(motor, motor.CW)
            motor.current_step = 445
            return True

    def move_motor(self, motor, direction):
        dir_pin = motor.DIR
        step_pin = motor.STEP
        GPIO.output(dir_pin, direction)
        for x in range(10):
            motor.new_current_step(x, direction)
            GPIO.output(step_pin, GPIO.HIGH)
            sleep(self.default_speed)
            GPIO.output(step_pin, GPIO.LOW)
            sleep(self.default_speed)

