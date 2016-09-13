from kivy.app import App
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty
from kivy.logger import Logger


Builder.load_file('ajuste.kv')
Builder.load_file('informacion.kv')
Builder.load_file('menu.kv')


class LifeGo(AnchorLayout):
    temperaturaDeseada = ObjectProperty()

    def __init__(self, **kwargs):
        super(LifeGo, self).__init__(**kwargs)
        self.temperaturaDeseada = 4


    def disminuirTemperaturaDeseada(self):
        self.temperaturaDeseada -= 1

        Logger.info(str(self.temperaturaDeseada))

    def aumentarTemperaturaDeseada(self):
        self.temperaturaDeseada += 1
        Logger.info(str(self.temperaturaDeseada))


class LifeGoApp(App):
    def build(self):
        return LifeGo()

if __name__ == '__main__':
    LifeGoApp().run()