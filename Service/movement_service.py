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
    active = False

    def __init__(self):
        print("init movement service")
        GPIO.output(self.stepper_motor_base.SLEEP, GPIO.HIGH)
        GPIO.output(self.stepper_motor_first_axis.SLEEP, GPIO.HIGH)
        self.stepper_motor_first_axis.init_stop_switches(
            Button(11, ButtonType.STOPS_WITCH, Position.FIRST_AXIS_LEFT, None),
            Button(5, ButtonType.STOPS_WITCH, Position.FIRST_AXIS_RIGHT, None))

    def moving_to_new_step(self, motor, direction, speed, pin_left, pin_right):
        print('Moving motor')
        dir_pin = motor.DIR
        step_pin = motor.STEP
        GPIO.output(dir_pin, direction)
        GPIO.output(motor.SLEEP, GPIO.HIGH)
        count = 0
        while self.active:
            motor.new_current_step(count + 1, direction)
            GPIO.output(step_pin, GPIO.HIGH)
            sleep(speed)
            GPIO.output(step_pin, GPIO.LOW)
            sleep(speed)
            count = count + 1
            if self.first_axis_stop_switch_check(motor, pin_left, pin_right):
                GPIO.output(motor.SLEEP, GPIO.LOW)
                sleep(1)
                self.active = False
                break
        print("New motor step position: ", motor.current_step)

    def first_axis_stop_switch_check(self, motor, pin_left, pin_right):
        if pin_left != '' and GPIO.input(pin_left):
            print("Left stop switch has been pressed")
            self.move_motor(motor, motor.CCW)
            motor.current_step = 0
            return True
        elif pin_right != '' and GPIO.input(pin_right):
            print("Right stop switch has been pressed")
            self.move_motor(motor, motor.CW)
            motor.current_step = motor.DEFAULT_MAX_STEP
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
