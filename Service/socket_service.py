import socket

from Domain.Enum.control_buttons_enum import ControlButton
from Service.control_board_service import ControlBoardService


class Socket(object):
    control_board = ControlBoardService()
    HOST = '127.0.0.1'
    PORT = 1337
    incoming_data = ''

    def __init__(self):
        self.control_board.first_time_run()
        while True:
            self.receive_socket()

    def receive_socket(self):
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv.bind(('0.0.0.0', self.PORT))
        serv.listen(5)
        while True:
            conn, addr = serv.accept()
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                conn.send(b'Thanks for the message sir')
                self.incoming_data = data
            conn.close()
            print("client disconnected")
            self.input_socket(self.incoming_data)

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
