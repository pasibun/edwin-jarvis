import socket

from Domain.Enum.control_buttons_enum import ControlButton
from Service.control_board_service import ControlBoardService


class Socket(object):
    control_board = ControlBoardService()
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind(('0.0.0.0', 1337))
    serv.listen(5)
    conn, addr = serv.accept()
    incoming_data = ''

    def __init__(self):
        try:
            self.control_board.first_time_run()
            while True:
                self.receive_socket()
        except KeyboardInterrupt:
            self.conn.close()
            print("client disconnected")

    def receive_socket(self):
        while True:
            data = self.conn.recv(4096)
            if not data:
                break
            self.conn.send(b'Thanks for the message sir')
            self.incoming_data = data
        print("Incoming message: ", self.incoming_data)
        self.input_socket(self.incoming_data.decode())

    def input_socket(self, input):
        value = ControlButton.FIRST_AXIS_LEFT
        if "right" in input.lower():
            value = ControlButton.BASE_RIGHT
        elif "left" in input.lower():
            value = ControlButton.BASE_LEFT
        elif "up" in input.lower():
            value = ControlButton.FIRST_AXIS_LEFT
        elif "down" in input.lower():
            value = ControlButton.FIRST_AXIS_RIGHT
        self.control_board.determine_motor_to_control(value)
