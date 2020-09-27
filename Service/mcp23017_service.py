import wiringpi2 as wiringpi
import time


class IOExpansionService(object):
    wiringpi.wiringPiSetup()
    pin_base = 65       # lowest available starting number is 65
    i2c_addr = 0x20     # A0, A1, A2 pins all wired to GND

    def __init__(self):
        wiringpi.mcp23017Setup(self.pin_base, self.i2c_addr)   # set up the pins and i2c address

        wiringpi.pinMode(80, 0)         # sets GPB7 to input
        wiringpi.pullUpDnControl(80, 2) # set internal pull-up