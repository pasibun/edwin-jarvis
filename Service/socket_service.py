import socket

from Domain.Enum.control_buttons_enum import ControlButton
from Service.control_board_service import ControlBoardService


class Socket(object):
    control_board = ControlBoardService()
    HOST = '127.0.0.1'
    PORT = 1337

    def __init__(self):
        self.control_board.first_time_run()
        while True:
            self.receive_socket()

    def receive_socket(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)
                    print(data)
                    self.input_socket(data)

    def input_socket(self, input):
        value = ControlButton.FIRST_AXIS_LEFT
        if input.lower() == "right":
            value = ControlButton.BASE_RIGHT
        elif input.lower() == "left":
            value = ControlButton.BASE_LEFT
        elif input.lower() == "up":
            value = ControlButton.FIRST_AXIS_LEFT
        elif input.lower() == "down":
            value = ControlButton.FIRST_AXIS_RIGHT
        self.control_board.determine_motor_to_control(value)
