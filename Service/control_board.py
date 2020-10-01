from Domain.button import Button


class ControlBoard(object):
    base_left = Button(37, 'baseLeft')  # GPIO26
    base_right = Button(35, 'baseRight')  # GPIO19
    first_left = Button(33, 'firstLeft')  # GPIO13
    first_right = Button(31, 'firstRight')  # GPIO6
