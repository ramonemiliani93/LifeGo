import os, sys
sys.path.insert(0, '/home/pi/Documents/LifeGo/LifeGo/Control')
import pid
import pwm
import Adafruit_DHT
import RPi.GPIO as GPIO
from time import sleep

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty
from kivy.logger import Logger
from kivy.clock import Clock

Builder.load_file('ajuste.kv')
Builder.load_file('informacion.kv')
Builder.load_file('menu.kv')


class LifeGo(AnchorLayout):
    temperaturaDeseada = ObjectProperty()

    def __init__(self, **kwargs):
        super(LifeGo, self).__init__(**kwargs)
        self.temperaturaDeseada = 4
        self.fan = None
        self.PID = None
        self.sensor = None
        self.pin = None

    def init(self):
        self.sensor = Adafruit_DHT.AM2302
        self.pin = 23

        Logger.info('va bien') #borrar esto

        self.PID = pid.PID(-60, -0.02, 0, Integrator_max=100, Integrator_min=-100)
        self.PID.setPoint(self.temperaturaDeseada)

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(21, GPIO.OUT)

        GPIO.output(16, GPIO.HIGH)
        GPIO.output(21, GPIO.LOW)

        self.fan = pwm.PWM(500, 0, 0, 12)

    def disminuirTemperaturaDeseada(self):
        self.temperaturaDeseada -= 1
        self.PID.setPoint(self.temperaturaDeseada)
        Logger.info(str(self.temperaturaDeseada))

    def aumentarTemperaturaDeseada(self):
        self.temperaturaDeseada += 1
        self.PID.setPoint(self.temperaturaDeseada)
        Logger.info(str(self.temperaturaDeseada))

    def updateSensor(self, dt):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        Logger.info(str(temperature)) #borrar esto
        Ciclo = (self.PID.update(temperature)/24)*100
        Logger.info(str(Ciclo))
        try :
                self.fan.setCycle(Ciclo)

        except :
                print('No se pudo leer el sensor')

class LifeGoApp(App):

    def build(self):
        lifego = LifeGo()
        lifego.init()
        Clock.schedule_interval(lifego.updateSensor, 30)
        return lifego

if __name__ == '__main__':
    LifeGoApp().run()