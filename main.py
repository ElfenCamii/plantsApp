from kivy.config import Config
# La configuración debe ir ANTES de importar cualquier cosa de KivyMD
Config.set('graphics', 'width', '412')
Config.set('graphics', 'height', '915')
Config.set('graphics', 'resizable', False)

from kivy.core.window import Window
from gui import RegandoAndo # Importamos la lógica desde el nuevo archivo

import os
os.environ['KIVY_NO_ARGS'] = '1' # Evita conflictos de argumentos
# Esto silencia los logs de tipo WARNING de la consola
from kivy.logger import Logger
import logging
Logger.setLevel(logging.ERROR)

if __name__ == "__main__":
    Window.top = 40
    Window.left = -500
    # Aquí es donde ocurre la magia:
    RegandoAndo().run()