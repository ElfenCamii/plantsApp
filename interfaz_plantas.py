from kivy.config import Config
# 1. Configuración de pantalla (DEBE IR ANTES DE CUALQUIER OTRO IMPORT DE KIVY)
# Emulamos la proporción de un S23 Ultra (aprox 412x915)
Config.set('graphics', 'width', '412')
Config.set('graphics', 'height', '915')
Config.set('graphics', 'resizable', False)

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.core.window import Window

import data
import functions

# 2. Centramos la ventana en tu monitor de PC
Window.top = 100
Window.left = 500

class AppPlantas(MDApp):
    def build(self):
        # Configuración estética global
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        
        pantalla = MDScreen()
        scroll = MDScrollView()

        # Contenedor de cuadrícula (2 columnas)
        self.contenedor_grid = MDGridLayout(
            cols=2, 
            spacing=dp(12), 
            padding=dp(12),
            adaptive_height=True 
        )

        self.cargar_inventario()

        scroll.add_widget(self.contenedor_grid)
        pantalla.add_widget(scroll)
        return pantalla

    def cargar_inventario(self):
        self.contenedor_grid.clear_widgets()
        plantas = data.get_all_plants()

        for p in plantas:
            tutor_raw = str(p[2]).lower().strip()
            tiene_tutor = tutor_raw in ["si", "sí", "s"]
            porcentaje_maceta = functions.obtener_estado_riego(p[5], p[4])
            
            # 1. LA TARJETA CUADRADA DINÁMICA
            tarjeta = MDCard(
                orientation='vertical',
                padding=dp(10),
                size_hint=(1, None), # Ocupa todo el ancho de la columna
                # AQUÍ ESTÁ EL TRUCO: La altura será igual al ancho
                height=self.contenedor_grid.width / 2 - dp(20), 
                radius=[dp(20)],
                elevation=2,
                ripple_behavior=True 
            )
            
            # Para asegurar que se actualice si cambias el tamaño de ventana
            tarjeta.bind(width=lambda instance, value: setattr(instance, 'height', value))

            # 2. TÍTULO Y ESPECIE (Compacto)
            titulo_especie = MDLabel(
                text=f"[b]{p[0]}[/b]\n[size=10]{p[1]}[/size]",
                markup=True,
                halign="center",
                adaptive_height=True,
                line_height=0.9
            )

            # 3. ICONO (Un poco más pequeño para que quepa en el cuadrado)
            ruta_imagen = "con_tutor.png" if tiene_tutor else "sin_tutor.png"
            imagen_planta = Image(
                source=ruta_imagen,
                size_hint=(None, None),
                size=(dp(80), dp(80)), # Bajamos a 80 para ganar espacio
                pos_hint={"center_x": 0.5}
            )

            # --- SECCIÓN MACETA ---
            barra_maceta = MDProgressBar(
                value=porcentaje_maceta,
                color=self.theme_cls.primary_color,
                size_hint_x=0.9,
                pos_hint={"center_x": 0.5},
                height=dp(6),
                size_hint_y=None
            )
            fila_maceta = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(14))
            fila_maceta.add_widget(MDLabel(text="M", font_style="Caption", theme_text_color="Secondary", size_hint_x=0.2))
            fila_maceta.add_widget(MDLabel(text=f"{porcentaje_maceta}%", font_style="Caption", halign="right"))

            # --- SECCIÓN TUTOR ---
            if tiene_tutor:
                porcen_tutor = functions.obtener_estado_riego(p[6], p[3])
                val_tutor = porcen_tutor
                txt_tutor = f"{porcen_tutor}%"
                col_tutor = (0.6, 0.4, 0.2, 1)
            else:
                val_tutor = 0
                txt_tutor = "No"
                col_tutor = (0.8, 0.8, 0.8, 1)

            barra_tutor = MDProgressBar(
                value=val_tutor,
                color=col_tutor,
                size_hint_x=0.9,
                pos_hint={"center_x": 0.5},
                height=dp(6),
                size_hint_y=None
            )
            fila_tutor = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(14))
            fila_tutor.add_widget(MDLabel(text="T", font_style="Caption", theme_text_color="Secondary", size_hint_x=0.2))
            fila_tutor.add_widget(MDLabel(text=txt_tutor, font_style="Caption", halign="right"))

            # 4. CONSTRUCCIÓN
            tarjeta.add_widget(titulo_especie)
            tarjeta.add_widget(imagen_planta)
            
            # Espaciador automático
            tarjeta.add_widget(MDLabel(text="", size_hint_y=1))
            
            tarjeta.add_widget(barra_maceta)
            tarjeta.add_widget(fila_maceta)
            
            tarjeta.add_widget(MDLabel(size_hint_y=None, height=dp(4))) # Espacio mínimo
            
            tarjeta.add_widget(barra_tutor)
            tarjeta.add_widget(fila_tutor)

            self.contenedor_grid.add_widget(tarjeta)

if __name__ == "__main__":
    AppPlantas().run()