from kivy.app import App
from kivy.uix.button import Button
from kivy.atlas import Atlas

class TestApp(App):
      def build(self):
            atlas = Atlas('/home/pi/kivy/kivy/data/images/defaulttheme.atlas')
            return Button(text='LifeGo: mas muerte, mas vida :)')

TestApp().run()
