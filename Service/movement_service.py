from time import sleep

import RPi.GPIO as GPIO
import threading

from Domain.Enum.button_type_enum import ButtonType
from Domain.Enum.position_enum import Position
from Domain.button import Button
from Domain.stepper_motor import StepperMotor
from Service.mcp_driver_service import IOExpander


class MovementService(object):
    io_expander = IOExpander()
    default_speed = 0.001
    stepper_motor_base = StepperMotor(16, 12, 15, (7, 8, 25), '1/4')
    stepper_motor_first_axis = StepperMotor(21, 20, 14, (24, 23, 18), '1/4')

    motor = None
    direction = None
    speed = None
    pin_left = None
    pin_right = None

    active = False

    def __init__(self):
        print("init movement service")
        GPIO.output(self.stepper_motor_base.SLEEP, GPIO.HIGH)
        GPIO.output(self.stepper_motor_first_axis.SLEEP, GPIO.HIGH)
        self.stepper_motor_first_axis.init_stop_switches(
            Button(11, ButtonType.STOPS_WITCH, Position.FIRST_AXIS_LEFT, None),
            Button(5, ButtonType.STOPS_WITCH, Position.FIRST_AXIS_RIGHT, None))

    def start_process_moving(self, motor, direction, speed, pin_left, pin_right):
        self.motor = motor
        self.direction = direction
        self.speed = speed
        self.pin_left = pin_left
        self.pin_right = pin_right

        print(print(GPIO.input(pin_left)))
        print(print(GPIO.input(pin_right)))

        t = threading.Thread(target=self.moving_motor)
        t.start()

    def moving_motor(self):
        try:
            self.io_expander.write_digital(self.io_expander.led_pin, 1)
            print('Thread: Moving motor')
            dir_pin = self.motor.DIR
            step_pin = self.motor.STEP
            GPIO.output(dir_pin, self.direction)
            GPIO.output(self.motor.SLEEP, GPIO.HIGH)
            count = 0
            while self.active:
                self.motor.new_current_step(count + 1, self.direction)
                GPIO.output(step_pin, GPIO.HIGH)
                sleep(self.speed)
                GPIO.output(step_pin, GPIO.LOW)
                sleep(self.speed)
                count = count + 1
                if self.first_axis_stop_switch_check(self.motor, self.pin_left, self.pin_right):
                    GPIO.output(self.motor.SLEEP, GPIO.LOW)
                    sleep(1)
                    break
            self.io_expander.write_digital(self.io_expander.led_pin, 0)
            print("Thread: New motor step position: ", self.motor.current_step)
            self.active = False
        except Exception:
            print("ERROR: moving_to_new_step, Er ging iets mis..")
            self.active = False

    def first_axis_stop_switch_check(self, motor, pin_left, pin_right):
        if pin_left != '' and GPIO.input(pin_left):
            print("Thread: Left stop switch has been pressed")
            self.move_motor_ten_steps(motor, motor.CCW)
            motor.current_step = 0
            return True
        elif pin_right != '' and GPIO.input(pin_right):
            print("Thread: Right stop switch has been pressed")
            self.move_motor_ten_steps(motor, motor.CW)
            motor.current_step = motor.DEFAULT_MAX_STEP
            return True

    def move_motor_ten_steps(self, motor, direction):
        dir_pin = motor.DIR
        step_pin = motor.STEP
        GPIO.output(dir_pin, direction)
        for x in range(10):
            motor.new_current_step(x, direction)
            GPIO.output(step_pin, GPIO.HIGH)
            sleep(self.default_speed)
            GPIO.output(step_pin, GPIO.LOW)
            sleep(self.default_speed)
