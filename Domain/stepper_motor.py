import RPi.GPIO as GPIO


class StepperMotor(object):
    stop_switch_left = None
    stop_switch_right = None
    DIR = 0
    STEP = 0
    SLEEP = 0
    MICRO_STEPPING = []
    CW = 1  # Clockwise Rotation
    CCW = 0  # Counterclockwise Rotation
    current_step = 458
    DEFAULT_MAX_STEP = 458

    RESOLUTION = {'Full': (0, 0, 0),
                  'Half': (1, 0, 0),
                  '1/4': (0, 1, 0),
                  '1/8': (1, 1, 0),
                  '1/16': (0, 0, 1),
                  '1/32': (1, 0, 1)}

    def __init__(self, dir, step, sleep, micro, resolution):
        self.DIR = dir
        self.STEP = step
        self.SLEEP = sleep
        self.MICRO_STEPPING = micro
        GPIO.setmode(GPIO.BCM)
        self.init_gpio_pins()
        GPIO.output(self.MICRO_STEPPING, self.RESOLUTION[resolution])

    def init_stop_switches(self, stop_switch_left, stop_switch_right):
        self.stop_switch_left = stop_switch_left
        self.stop_switch_right = stop_switch_right

    def init_gpio_pins(self):
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.STEP, GPIO.OUT)
        GPIO.setup(self.SLEEP, GPIO.OUT)
        GPIO.output(self.DIR, self.CW)
        GPIO.setup(self.MICRO_STEPPING, GPIO.OUT)
        GPIO.output(self.STEP, GPIO.LOW)
        GPIO.output(self.SLEEP, GPIO.LOW)

    def new_current_step(self, step, direction):
        if direction == self.CW:
            self.current_step = self.current_step - step
        elif direction == self.CCW:
            self.current_step = self.current_step + step
