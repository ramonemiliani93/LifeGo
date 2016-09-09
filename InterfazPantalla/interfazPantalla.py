import kivy

kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label

class MyApp(App):
    def build(self):
        button = Button(text="Control de temperatura", font_size = 40, background_color=(0,0,1,1))
        return button

if __name__ == '__main__':
    MyApp().run()
