import paho.mqtt.client as mqtt

from Domain.Enum.control_buttons_enum import ControlButton
from Service.control_board_service import ControlBoardService


class MqttService(object):
    client = mqtt.Client("edwin-jarvis")
    control_board = ControlBoardService()
    MQTT_HOST = "10.0.0.109"
    MQTT_USERNAME = ""
    MQTT_PASSWORD = ""
    MQTT_TOPIC_BASE = "edwin/jarvis/control/base/set"
    MQTT_TOPIC_FIRST_AXIS = "edwin/jarvis/control/first/axis/set"

    def __init__(self):
        print("init mqtt service")
        self.make_connection()
        self.subscribe_to_topics()
        self.control_board.first_time_run()

    def make_connection(self):
        self.enter_credentials()
        print("Making connection with mqtt service.")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(username=self.MQTT_USERNAME, password=self.MQTT_PASSWORD)
        self.client.connected_flag = False
        self.client.connect(self.MQTT_HOST, port=1883, keepalive=60, bind_address="")
        self.client.loop_forever()  # loop_start

    def enter_credentials(self):
        try:
            print("Enter username for the MQTT connection:")
            self.MQTT_USERNAME = input()
            print("Enter password for the MQTT connection:")
            self.MQTT_PASSWORD = input()
            print("Press y to confirm.")
            result = input()
            if not result.isdigit() and result.lower() != "y":
                print("Lets try that again..")
                self.enter_credentials()
        except ValueError:
            print("Wrong fucking input retard.")

    def subscribe_to_topics(self):
        print("Subscribing to topic: ", self.MQTT_TOPIC_BASE)
        self.client.subscribe(self.MQTT_TOPIC_BASE)
        print("Subscribing to topic: ", self.MQTT_TOPIC_FIRST_AXIS)
        self.client.subscribe(self.MQTT_TOPIC_FIRST_AXIS)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.client.connected_flag = True
            print("connected ok")
        else:
            print("Bad connection Returned code= ", rc)

    def on_message(self, client, userdata, message):
        print("message received ", str(message.payload.decode("utf-8")))
        value = ControlButton.FIRST_AXIS_LEFT
        if str(message.payload.decode("utf-8")).lower() == "right":
            value = ControlButton.BASE_RIGHT
        elif str(message.payload.decode("utf-8")).lower() == "left":
            value = ControlButton.BASE_LEFT
        elif str(message.payload.decode("utf-8")).lower() == "up":
            value = ControlButton.FIRST_AXIS_LEFT
        elif str(message.payload.decode("utf-8")).lower() == "down":
            value = ControlButton.FIRST_AXIS_RIGHT
        self.control_board.determine_motor_to_control(value)
