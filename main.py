from kivy.config import Config

Config.set('graphics', 'width', '412')
Config.set('graphics', 'height', '915')
Config.set('graphics', 'resizable', False)

from kivy.core.window import Window
from gui import RegandoAndo
import os

Window.softinput_mode = "below_target"
os.environ['KIVY_NO_ARGS'] = '1'
from kivy.logger import Logger
import logging
Logger.setLevel(logging.ERROR)

if __name__ == "__main__":
    Window.top = 40
    Window.left = -500
    
    RegandoAndo().run()