import logging

import RPi.GPIO as GPIO

from Service.socket_service import Socket


def clean_up():
    print("Exiting program.")
    GPIO.output(14, GPIO.LOW)
    GPIO.output(15, GPIO.LOW)


if __name__ == "__main__":
    try:
        logging.basicConfig(filename='logging.log', level=logging.INFO, format='%(asctime)s %(message)s')
        logging.info("Starting application. Saving logs in ~/logging.log")
        # GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        # MqttService()
        socket = Socket()
        clean_up()
    except KeyboardInterrupt:
        clean_up()
