class StepperMotor(object):
    DIR = 0  # Direction GPIO Pin
    STEP = 0  # Step GPIO Pin
    CW = 1  # Clockwise Rotation
    CCW = 0  # Counterclockwise Rotation
    SPR = 200  # Steps per Revolution (360 / 1.8)

    def __init__(self, dir, step):
        self.DIR = dir
        self.STEP = step