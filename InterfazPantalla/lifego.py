import os, sys
sys.path.insert(0, '/home/pi/Documents/LifeGo/LifeGo/Control')
sys.path.insert(0, '/home/pi/Documents/LifeGo/LifeGo/Sensores')

import control
import ambiente
import threading

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
        self.control = control.Control()
        self.ambiente = ambiente.TemperaturaAmbiente()
        self.ambiente.start()
        threading.Thread(target=control.actualizar, args=(ambiente,)).start()
        self.temperaturaDeseada = 4
        control.setPoint(self.temperaturaDeseada)

    def disminuirTemperaturaDeseada(self):
        self.temperaturaDeseada -= 1
        self.control.setPoint(self.temperaturaDeseada)
        Logger.info(str(self.temperaturaDeseada))

    def aumentarTemperaturaDeseada(self):
        self.temperaturaDeseada += 1
        self.control.setPoint(self.temperaturaDeseada)
        Logger.info(str(self.temperaturaDeseada))


class LifeGoApp(App):

    def build(self):
        return LifeGo()

if __name__ == '__main__':
    LifeGoApp().run()