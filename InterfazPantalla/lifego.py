import os, sys
sys.path.insert(0, '/home/pi/Documents/LifeGo/LifeGo/Control')
sys.path.insert(0, '/home/pi/Documents/LifeGo/LifeGo/Sensores')

import control
import ambiente
import organo
import threading
from time import sleep

import kivy
kivy.require('1.9.0')


from kivy.app import App
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.logger import Logger
from kivy.clock import Clock


Builder.load_file('ajuste.kv')
Builder.load_file('informacion.kv')
Builder.load_file('menu.kv')


class LifeGo(AnchorLayout):
    temperaturaDeseada = ObjectProperty()
    temperaturaActual = StringProperty()
    humedadActual = StringProperty()
    temperaturaOrganoActual = StringProperty()

    def __init__(self, **kwargs):
        super(LifeGo, self).__init__(**kwargs)
        self.controlT = control.Control()
        self.ambienteS = ambiente.TemperaturaAmbiente()
        self.organoS = organo.TemperaturaOrgano()
        
        self.ambienteS.start()
        self.organoS.start()
        threading.Thread(target=self.controlT.actualizar, args=(self.ambienteS,)).start()
        
        self.temperaturaActual = str('no ha iniciado')
        self.humedadActual = str('no ha iniciado')
        self.temperaturaOrganoActual = str('no ha iniciado')
        
        self.temperaturaDeseada = 4
        self.controlT.setPoint(self.temperaturaDeseada)

    def disminuirTemperaturaDeseada(self):
        self.temperaturaDeseada -= 1
        self.controlT.setPoint(self.temperaturaDeseada)
        Logger.info(str(self.temperaturaDeseada))

    def aumentarTemperaturaDeseada(self):
        self.temperaturaDeseada += 1
        self.controlT.setPoint(self.temperaturaDeseada)
        Logger.info(str(self.temperaturaDeseada))

    def updateInterfaz(self):
        while True:
            sleep(5)
            ttemporal = self.ambienteS.getTemperaturaAmbiente()
            htemporal = self.ambienteS.getHumedadAmbiente()
            torganotemporal = self.organoS.getTemperaturaOrgano()
            if ttemporal is None:
                self.temperaturaActual = str('...')
            else:
                self.temperaturaActual = '{0:.1f}'.format(round(ttemporal, 1))
            if htemporal is None:
                self.humedadActual = str('...')
            else:
                self.humedadActual = '{0:.1f}'.format(round(htemporal, 1))
            if torganotemporal is None:
                self.temperaturaOrganoActual = str('...')
            else:
                self.temperaturaOrganoActualhumedadActual = '{0:.1f}'.format(round(torganotemporal, 1))

class LifeGoApp(App):

    def build(self):
        lf = LifeGo()
        threading.Thread(target=lf.updateInterfaz).start()
        return lf

if __name__ == '__main__':
    LifeGoApp().run()
