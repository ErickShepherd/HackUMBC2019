#!/usr/bin/env python

# Third party imports.
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window

# Window configuration.
Window.size = (int(1080 * 0.25), int(1920 * 0.25))


class MyApp(App):

    def build(self):
        
        return Label(text = "Hello world")


if __name__ == "__main__":
    
    MyApp().run()
