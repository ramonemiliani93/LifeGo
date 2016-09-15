import RPi.GPIO as GPIO
import pid


class Control(threading.Thread):
    def __init__(self):
        self.pin = 23