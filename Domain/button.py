import RPi.GPIO as GPIO


class Button(object):
    TYPE = ''
    POSITION = ''
    CONTROL = ''
    PIN = 0

    def __init__(self, gpio, button_type, position, control):
        self.PIN = gpio
        self.TYPE = button_type
        self.POSITION = position
        self.CONTROL = control
        GPIO.setmode(GPIO.BCM)
        self.init_gpio_pins()

    def init_gpio_pins(self):
        GPIO.setup(self.PIN, GPIO.IN)
