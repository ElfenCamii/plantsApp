from kivy.config import Config
Config.set('graphics', 'width', '412')
Config.set('graphics', 'height', '915')
Config.set('graphics', 'resizable', False)

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDFloatingActionButton, MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDSwitch
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.core.window import Window

import data
import functions

Window.top = 40
Window.left = 500

class AppPlantas(MDApp):
    dialogo = None 
    imagen_seleccionada = "assets/img_planta_01.png"
    lista_botones_iconos = []

    def build(self):
        data.init_db() # Inicializar DB al arrancar
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        
        self.pantalla_principal = MDScreen()
        layout_base = MDFloatLayout()

        scroll = MDScrollView(size_hint=(1, 1))
        self.contenedor_grid = MDGridLayout(
            cols=2, spacing=dp(12), padding=dp(12), adaptive_height=True 
        )

        self.cargar_inventario()

        boton_agregar = MDFloatingActionButton(
            icon="plus",
            md_bg_color=self.theme_cls.primary_color,
            pos_hint={'center_x': 0.85, 'center_y': 0.08},
            on_release=self.abrir_formulario 
        )

        scroll.add_widget(self.contenedor_grid)
        layout_base.add_widget(scroll)
        layout_base.add_widget(boton_agregar)
        
        self.pantalla_principal.add_widget(layout_base)
        return self.pantalla_principal

    def abrir_formulario(self, *args):
        self.lista_botones_iconos = []
        
        # 1. Contenedor principal que permite scroll si falta espacio
        scroll = MDScrollView(size_hint_y=None, height=dp(450)) # Altura fija de la zona de datos
        
        # 2. Contenedor de los widgets con espaciado real
        self.contenido = BoxLayout(
            orientation="vertical", 
            spacing="20dp", # Más espacio entre campos
            padding=[dp(20), dp(20), dp(20), dp(20)], 
            size_hint_y=None
        )
        self.contenido.bind(minimum_height=self.contenido.setter('height'))

        # Campos de texto con margen extra
        self.campo_nombre = MDTextField(hint_text="Nombre de la planta", mode="rectangle")
        self.campo_especie = MDTextField(hint_text="Especie", mode="rectangle")
        self.campo_frec_m = MDTextField(hint_text="Riego Maceta (días)", text="7", input_filter="int", mode="rectangle")
        
        # Fila del Tutor optimizada
        fila_tutor = BoxLayout(
            orientation="horizontal", 
            size_hint_y=None, 
            height="48dp",
            padding=[0, 0, dp(15), 0] # <--- Agregamos 15dp de margen a la derecha
        )
        fila_tutor.add_widget(MDLabel(text="¿Tiene tutor?", theme_text_color="Secondary"))
        
        # El Switch ahora no se deformará
        self.switch_tutor = MDSwitch(
            active=False, 
            pos_hint={'center_y': 0.5},
            size_hint=(None, None), # Desactivamos el estiramiento automático
            size=(dp(48), dp(32))   # Le damos un tamaño fijo estándar
        )
        self.switch_tutor.bind(active=self.mostrar_campo_tutor)
        fila_tutor.add_widget(self.switch_tutor)
        
        # Campo de Riego Tutor (Oculto al inicio)
        self.campo_frec_t = MDTextField(
            hint_text="Riego Tutor (días)", text="15", 
            input_filter="int", mode="rectangle",
            size_hint_y=None, height=0, opacity=0
        )
        
        # Selector de Iconos
        label_selector = MDLabel(text="Selecciona un icono:", font_style="Caption", theme_text_color="Secondary")
        selector_grid = MDGridLayout(cols=3, spacing="15dp", adaptive_height=True)
        
        for i in range(1, 10):
            nombre_img = f"assets/img_planta_0{i}.png"
            btn_img = MDIconButton(
                icon=nombre_img, icon_size=dp(40),
                on_release=lambda x, path=nombre_img: self.seleccionar_icono(path, x)
            )
            self.lista_botones_iconos.append(btn_img)
            selector_grid.add_widget(btn_img)

        # Agregamos todo al contenido
        self.contenido.add_widget(self.campo_nombre)
        self.contenido.add_widget(self.campo_especie)
        self.contenido.add_widget(self.campo_frec_m)
        self.contenido.add_widget(fila_tutor)
        self.contenido.add_widget(self.campo_frec_t)
        self.contenido.add_widget(label_selector)
        self.contenido.add_widget(selector_grid)

        scroll.add_widget(self.contenido)

        self.dialogo = MDDialog(
            title="Nueva Planta",
            type="custom",
            content_cls=scroll, # <--- Ahora el contenido es el Scroll
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=lambda x: self.dialogo.dismiss()),
                MDRaisedButton(text="GUARDAR", md_bg_color=self.theme_cls.primary_color, on_release=self.guardar_nueva_planta)
            ],
        )
        self.dialogo.open()

    
    def mostrar_campo_tutor(self, instance, value):
        if value: # Si el switch está activo
            self.campo_frec_t.height = dp(60) # Le damos altura
            self.campo_frec_t.opacity = 1      # Lo hacemos visible
            self.campo_frec_t.size_hint_y = None
        else:
            self.campo_frec_t.height = 0
            self.campo_frec_t.opacity = 0
            self.campo_frec_t.size_hint_y = None

    def seleccionar_icono(self, ruta, instancia):
        self.imagen_seleccionada = ruta
        for btn in self.lista_botones_iconos:
            btn.md_bg_color = [0, 0, 0, 0]
        instancia.md_bg_color = self.theme_cls.primary_light

    def guardar_nueva_planta(self, *args):
        nombre = self.campo_nombre.text
        especie = self.campo_especie.text
        tutor = "si" if self.switch_tutor.active else "no"
        
        frec_m = int(self.campo_frec_m.text) if self.campo_frec_m.text.isdigit() else 7
        # Si el tutor está activo, usamos lo que diga el campo; si no, 0.
        frec_t = int(self.campo_frec_t.text) if (tutor == "si" and self.campo_frec_t.text.isdigit()) else 0
        
        data.insert_plant(nombre, especie, tutor, frec_t, frec_m, self.imagen_seleccionada)
        self.dialogo.dismiss()
        self.cargar_inventario()

    def cargar_inventario(self):
        self.contenedor_grid.clear_widgets()
        plantas = data.get_all_plants()

        for p in plantas:
            # p[0]=id, p[1]=nom, p[2]=esp, p[3]=tut, p[4]=f_t, p[5]=f_m, p[6]=l_m, p[7]=l_t, p[8]=img
            tiene_tutor = str(p[3]).lower() == "si"
            porcentaje_m = functions.obtener_estado_riego(p[6], p[5])
            
            tarjeta = MDCard(orientation='vertical', padding=dp(10), size_hint=(1, None), radius=[dp(20)], elevation=2)
            tarjeta.bind(width=lambda instance, value: setattr(instance, 'height', value))

            tarjeta.add_widget(MDLabel(text=f"[b]{p[1]}[/b]\n[size=10]{p[2]}[/size]", markup=True, halign="center", adaptive_height=True))
            
            tarjeta.add_widget(Image(source=p[8], size_hint=(None, None), size=(dp(80), dp(80)), pos_hint={"center_x": 0.5}))

            # Barra Maceta
            tarjeta.add_widget(MDProgressBar(value=porcentaje_m, size_hint_x=0.9, pos_hint={"center_x": 0.5}))
            tarjeta.add_widget(MDLabel(text=f"M: {porcentaje_m}%", font_style="Caption", halign="center"))

            # Barra Tutor
            if tiene_tutor:
                porcen_t = functions.obtener_estado_riego(p[7], p[4])
                tarjeta.add_widget(MDProgressBar(value=porcen_t, color=(0.6, 0.4, 0.2, 1), size_hint_x=0.9, pos_hint={"center_x": 0.5}))
                tarjeta.add_widget(MDLabel(text=f"T: {porcen_t}%", font_style="Caption", halign="center"))

            self.contenedor_grid.add_widget(tarjeta)

if __name__ == "__main__":
    AppPlantas().run()