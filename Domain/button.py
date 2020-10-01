class Button(object):
    NAME = ''
    PIN = 0

    def __init__(self, gpio, name):
        self.PIN = gpio
        self.NAME = name
