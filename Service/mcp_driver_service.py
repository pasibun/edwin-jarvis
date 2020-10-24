import wiringpi as wiringpi
from time import sleep


class IOExpander(object):
    pin_base = 65  # lowest available starting number is 65
    led_pin = 73
    i2c_addr = 0x20
    wiringpi.wiringPiSetup()

    def __init__(self):
        wiringpi.mcp23017Setup(self.pin_base, self.i2c_addr)
        wiringpi.pinMode(self.led_pin, 1)
        wiringpi.digitalWrite(self.led_pin, 1)
        sleep(1)
        wiringpi.digitalWrite(self.led_pin, 0)

    def write_digital(self, pin, state):
        wiringpi.digitalWrite(pin, state)
