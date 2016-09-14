#Si lo corre desde la Pi, use la TERMINAL!
import kivy
import os, sys
sys.path.insert(0, '/home/pi/Documents/LifeGo/LifeGo/Control')
import pid
import pwm
import Adafruit_DHT
import RPi.GPIO as GPIO
from time import sleep

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.logger import Logger

class MyApp(App):
    def build(self):
        button1 = Button(text='Start', size_hint_x=None, width=100)
        button1.bind(on_press = self.start_lifego)

        layout = GridLayout(cols=2, row_force_default=True, row_default_height=40)
        layout.add_widget(button1)
        layout.add_widget(Button(text='World 1'))
        layout.add_widget(Button(text='Hello 2', size_hint_x=None, width=100))
        layout.add_widget(Button(text='World 2'))
        return layout

    def on_start(self):

        sensor = Adafruit_DHT.AM2302
        pin = 23

        Logger.info('va bien') #borrar esto

        p = pid.PID(-60, -0.02, 0, Integrator_max=100, Integrator_min=-100)
        p.setPoint(8)

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(21, GPIO.OUT)

        GPIO.output(16, GPIO.HIGH)
        GPIO.output(21, GPIO.LOW)

        fan = pwm.PWM(500, 0, 0, 12)

    def start_lifego(self):
        fan.startPWM()
        try:
            while True:
                sleep(.5)
                os.system('clear')
                humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
                Ciclo = (p.update(temperature)/24)*100
                try :
                    fan.setCycle(Ciclo)
                except :
                    print('No se pudo leer el sensor')
                print(str(temperature))
                print(str(Ciclo))

        except KeyboardInterrupt:
          pass
#App.get_running_app().stop()
if __name__ == '__main__':
    MyApp().run()





##import kivy
##
##from kivy.app import App
##from kivy.uix.button import Button
##from kivy.logger import Logger
##
##class CoolApp(App):
##    icon = 'custom-kivy-icon.png'
##    title = 'Basic Application'
##
##    def build(self):
##        return Button(text='Hello World')
##
##    def on_start(self):
##        Logger.info('App: I\'m alive!')
##
##    def on_stop(self):
##        Logger.critical('App: Aaaargh I\'m dying!')
##
##if __name__ in ('__android__', '__main__'):
##    CoolApp().run()
