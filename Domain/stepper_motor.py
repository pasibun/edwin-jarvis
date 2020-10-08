import RPi.GPIO as GPIO


class StepperMotor(object):
    DIR = 0  # Direction GPIO Pin
    STEP = 0  # Step GPIO Pin
    MICRO_STEPPING = []
    CW = 1  # Clockwise Rotation
    CCW = 0  # Counterclockwise Rotation
    SPR = 200  # Steps per Revolution (360 / 1.8)
    current_step = 0

    RESOLUTION = {'Full': (0, 0, 0),
                  'Half': (1, 0, 0),
                  '1/4': (0, 1, 0),
                  '1/8': (1, 1, 0),
                  '1/16': (0, 0, 1),
                  '1/32': (1, 0, 1)}

    def __init__(self, dir, step, micro, resolution):
        self.DIR = dir
        self.STEP = step
        self.MICRO_STEPPING = micro
        self.init_gpio_pins()
        GPIO.output(self.MICRO_STEPPING, self.RESOLUTION[resolution])

    def init_gpio_pins(self):
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.STEP, GPIO.OUT)
        GPIO.output(self.DIR, self.CW)
        GPIO.output(self.STEP, GPIO.LOW)


    def new_current_step(self, step):
        self.current_step += step
