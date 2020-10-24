from time import sleep
import multiprocessing
from multiprocessing import Process, Value
import RPi.GPIO as GPIO
from Domain.button import Button
from Domain.Enum.button_type_enum import ButtonType
from Domain.Enum.position_enum import Position
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
    p1 = None

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

        self.p1 = multiprocessing.Process(target=self.moving_to_new_step)
        self.p1.deamon = True
        self.p1.start()

    def moving_to_new_step(self):
        self.io_expander.write_digital(self.io_expander.led_pin, 1)
        print('p1: Moving motor')
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
                self.active = False
                break
        self.io_expander.write_digital(self.io_expander.led_pin, 0)
        print("p1: New motor step position: ", self.motor.current_step)
        print("Terminating p1.")
        self.p1.terminate()

    def first_axis_stop_switch_check(self, motor, pin_left, pin_right):
        if pin_left != '' and GPIO.input(pin_left):
            print("p1: Left stop switch has been pressed")
            self.move_motor(motor, motor.CCW)
            motor.current_step = 0
            return True
        elif pin_right != '' and GPIO.input(pin_right):
            print("p1: Right stop switch has been pressed")
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
