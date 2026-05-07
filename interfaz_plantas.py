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
            # Lógica de datos (Limpieza de strings para el tutor)
            tutor_raw = str(p[2]).lower().strip()
            tiene_tutor = tutor_raw in ["si", "sí", "s"]
            porcentaje_maceta = functions.obtener_estado_riego(p[5], p[4])
            
            # 3. La Tarjeta (Altura fija de 320 para iconos de 100)
            tarjeta = MDCard(
                orientation='vertical',
                padding=[dp(15), dp(10), dp(15), dp(15)],
                size_hint_y=None,
                height=dp(320), 
                radius=[dp(20)],
                elevation=2,
                ripple_behavior=True 
            )

            # 4. Icono Personalizado (Cargando tus PNGs)
            ruta_imagen = "con_tutor.png" if tiene_tutor else "sin_tutor.png"
            imagen_planta = Image(
                source=ruta_imagen,
                size_hint=(None, None),
                size=(dp(100), dp(100)),
                pos_hint={"center_x": 0.5},
                allow_stretch=True
            )

            # Título (Nombre en negrita y especie pequeña)
            titulo = MDLabel(
                text=f"[b]{p[0]}[/b]\n[size=12]{p[1]}[/size]",
                markup=True,
                halign="center",
                adaptive_height=True
            )
            
            # --- SECCIÓN MACETA (Fila Horizontal para el %) ---
            fila_maceta = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(20))
            fila_maceta.add_widget(MDLabel(text="Maceta", font_style="Caption", theme_text_color="Secondary"))
            fila_maceta.add_widget(MDLabel(text=f"{porcentaje_maceta}%", font_style="Caption", halign="right", theme_text_color="Primary"))

            barra_maceta = MDProgressBar(
                value=porcentaje_maceta,
                color=self.theme_cls.primary_color,
                size_hint_x=1,
                height=dp(8),
                size_hint_y=None
            )

            # Agregamos widgets a la tarjeta en orden
            tarjeta.add_widget(imagen_planta)
            tarjeta.add_widget(MDLabel(size_hint_y=None, height=dp(5)))
            tarjeta.add_widget(titulo)
            tarjeta.add_widget(MDLabel(size_hint_y=None, height=dp(10)))
            tarjeta.add_widget(fila_maceta)
            tarjeta.add_widget(barra_maceta)

            # --- SECCIÓN TUTOR ---
            if tiene_tutor:
                porcen_tutor = functions.obtener_estado_riego(p[6], p[3])
                
                fila_tutor = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(20))
                fila_tutor.add_widget(MDLabel(text="Tutor", font_style="Caption", theme_text_color="Secondary"))
                fila_tutor.add_widget(MDLabel(text=f"{porcen_tutor}%", font_style="Caption", halign="right", theme_text_color="Primary"))

                barra_tutor = MDProgressBar(
                    value=porcen_tutor,
                    color=(0.6, 0.4, 0.2, 1), # Café
                    size_hint_x=1,
                    height=dp(8),
                    size_hint_y=None
                )
                
                tarjeta.add_widget(MDLabel(size_hint_y=None, height=dp(10)))
                tarjeta.add_widget(fila_tutor)
                tarjeta.add_widget(barra_tutor)
            else:
                # Si no hay tutor, añadimos un espacio flexible para mantener la alineación
                tarjeta.add_widget(MDLabel(text="", size_hint_y=1)) 

            self.contenedor_grid.add_widget(tarjeta)

if __name__ == "__main__":
    AppPlantas().run()