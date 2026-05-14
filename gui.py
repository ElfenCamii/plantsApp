from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDSwitch

from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.properties import NumericProperty, ColorProperty
from kivy.metrics import dp
from kivy.clock import Clock

import data
import os
from components import LongPressCard
from datetime import datetime

class CircularProgress(Widget):
    value = NumericProperty(100)
    color = ColorProperty([0, 1, 0, 1])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.draw, size=self.draw, value=self.draw)

    def draw(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            cx, cy = self.x + self.width / 2, self.y + self.height / 2
            radius = self.width / 2
            
            # Fondo gris circular
            Color(0.8, 0.8, 0.8, 0.3)
            Line(circle=(cx, cy, radius), width=dp(2))
            
            angle_start = 90
            
            if self.value >= 0:
                # Lógica normal (Verde/Vida): Sentido horario
                Color(*self.color)
                # Kivy dibuja antihorario por defecto, así que 90 - (porcentaje)
                angle_end = 90 - (max(0.1, self.value) / 100) * 360
                Line(circle=(cx, cy, radius, angle_end, angle_start), width=dp(3.5), cap='round')
            else:
                # Lógica de Deuda (Rojo): Sentido antihorario
                Color(1, 0, 0, 1) # Rojo puro
                # Convertimos el valor negativo a positivo para el cálculo (max 2 días = 100%)
                abs_value = min(100, abs(self.value))
                # Para que crezca al revés, sumamos al ángulo de inicio
                angle_end = 90 + (abs_value / 100) * 360
                Line(circle=(cx, cy, radius, angle_start, angle_end), width=dp(4), cap='round')

class RegandoAndo(MDApp):
    dialogo = None 
    modo_eliminar = False
    imagen_seleccionada = "assets/img_planta_01.png"
    

    def build(self):
        data.init_db()
        self.theme_cls.primary_palette = "Green"
        self.root = MDScreen()
        layout_principal = MDBoxLayout(orientation="vertical")

        scroll = MDScrollView(do_scroll_x=False)
        self.contenedor_grid = MDGridLayout(cols=2, spacing=dp(12), padding=dp(12), adaptive_height=True)
        
        self.cargar_inventario()
        scroll.add_widget(self.contenedor_grid)
        layout_principal.add_widget(scroll)

        self.nav_bar = MDBoxLayout(orientation="horizontal", md_bg_color=self.theme_cls.primary_color, height=dp(56), size_hint_y=None)
        self.renderizar_nav_bar()

        layout_principal.add_widget(self.nav_bar)
        self.root.add_widget(layout_principal)

        Clock.schedule_interval(lambda dt: self.cargar_inventario(), 60)

        return self.root

    def renderizar_nav_bar(self):
        self.nav_bar.clear_widgets()
        color_icon = [1, 0.3, 0.3, 1] if self.modo_eliminar else [1, 1, 1, 1]
        items = [("trash-can", self.activar_modo_eliminar), ("plus-circle", self.abrir_formulario), ("cog", lambda x: None)]
        for icon, func in items:
            area = MDFloatLayout(size_hint_x=0.33)
            btn = MDIconButton(icon=icon, theme_text_color="Custom", text_color=color_icon,
                               pos_hint={'center_x': 0.5, 'center_y': 0.5}, on_release=func)
            if icon == "plus-circle": btn.icon_size = dp(36)
            area.add_widget(btn)
            self.nav_bar.add_widget(area)

    def cargar_inventario(self):
        self.contenedor_grid.clear_widgets()
        plantas = data.get_all_plants()
        for p in plantas:
            # 1. Cálculos de vida
            porc_m = data.calcular_barra_vida(p[6], p[5])
            color_m = [0.2, 0.7, 0.3, 1] if porc_m >= 0 else [1, 0, 0, 1]
            
            # 2. Tarjeta Principal
            tarjeta = LongPressCard(
                orientation='vertical', padding=dp(10), size_hint=(1, None), 
                height=dp(250), radius=[dp(20)], elevation=2,
                on_long_press=lambda x, p_id=p[0]: self.abrir_editor(p_id)
            )
            # Solo abre opciones si NO estamos en modo eliminar
            tarjeta.bind(on_release=lambda x, p_id=p[0]: self.mostrar_opciones(p_id))
            
            # 3. Contenido visual
            tarjeta.add_widget(MDLabel(text=f"[b]{p[1]}[/b]", markup=True, halign="center", font_style="H6", size_hint_y=None, height=dp(30)))
            tarjeta.add_widget(MDLabel(text=p[2] if p[2] else " ", halign="center", font_style="Subtitle2", theme_text_color="Secondary", size_hint_y=None, height=dp(20)))
            tarjeta.add_widget(Image(source=p[8], size_hint=(1, None), height=dp(80), fit_mode="contain"))
            
            # 4. Contenedor de botones de riego
            layout_riego = MDBoxLayout(orientation="horizontal", spacing=dp(20), adaptive_size=True, pos_hint={"center_x": 0.5})
            
            # --- MACETA ---
            area_m = MDAnchorLayout(size_hint=(None, None), size=(dp(50), dp(50)))
            area_m.add_widget(CircularProgress(value=porc_m, color=color_m, size=(dp(46), dp(46))))

            # BOTÓN REFORZADO:
            btn_m = MDIconButton(
                icon="", 
                size_hint=(None, None), 
                size=(dp(50), dp(50)), # Que ocupe todo el círculo
                on_release=lambda x, p_id=p[0]: self.regar_planta(p_id, "maceta")
            )
            area_m.add_widget(btn_m)
            area_m.add_widget(MDLabel(text="M", font_style="Caption", halign="center"))
            layout_riego.add_widget(area_m)
            
            # --- TUTOR ---
            if p[3] == "si":
                porc_t = data.calcular_barra_vida(p[7], p[4])
                color_t = [0.6, 0.4, 0.2, 1] if porc_t >= 0 else [1, 0, 0, 1]
                area_t = MDAnchorLayout(size_hint=(None, None), size=(dp(50), dp(50)))
                area_t.add_widget(CircularProgress(value=porc_t, color=color_t, size=(dp(46), dp(46))))
                btn_t = MDIconButton(
                    icon="", size_hint=(None, None), size=(dp(46), dp(46)), 
                    on_release=lambda x, p_id=p[0]: self.regar_planta(p_id, "tutor")
                )
                area_t.add_widget(btn_t)
                area_t.add_widget(MDLabel(text="T", font_style="Caption", halign="center"))
                layout_riego.add_widget(area_t)

            tarjeta.add_widget(layout_riego)
            self.contenedor_grid.add_widget(tarjeta)

    def abrir_formulario(self, *args):
        self.imagen_seleccionada = "assets/img_planta_01.png"
        
        # Reducimos el scroll para dejar aire a los botones de abajo
        self.scroll_formulario = MDScrollView(size_hint_y=None, height=dp(340))
        
        self.layout_campos = MDBoxLayout(
            orientation="vertical", 
            spacing=dp(10), 
            size_hint_y=None, 
            padding=[dp(30), dp(30), dp(30), dp(20)]
        )
        self.layout_campos.bind(minimum_height=self.layout_campos.setter('height'))

        # --- CONTENIDO DEL FORMULARIO ---
        self.img_preview = Image(source=self.imagen_seleccionada, size_hint_y=None, height=dp(80))
        btn_img = MDRaisedButton(
            text="CAMBIAR IMAGEN", # Cambiado para que sea más claro
            pos_hint={"center_x": 0.5},
            on_release=self.mostrar_selector_imagenes
        )
        
        self.tf_nombre = MDTextField(
            hint_text="Nombre de la planta",
            mode="line"
        )
        self.tf_especie = MDTextField(
            hint_text="Especie",
            mode="line"
        )
        self.tf_freq_m = MDTextField(
            hint_text="Frecuencia Maceta (días)", 
            input_filter="int",
            mode="line"
        )
        self.tf_fecha_m = MDTextField(
            hint_text="Último riego Maceta (AAAA-MM-DD)", 
            text=datetime.now().strftime('%Y-%m-%d'),
            mode="line"
        )
        
        # Fila del Tutor mejorada
        row_tutor = MDBoxLayout(orientation="horizontal", adaptive_height=True, padding=[0, dp(10)])
        row_tutor.add_widget(MDLabel(text="¿Tiene Tutor?", theme_text_color="Secondary"))
        self.switch_tutor = MDSwitch(active=False)
        self.switch_tutor.bind(active=self.toggle_tutor_field)
        row_tutor.add_widget(self.switch_tutor)
        
        self.tf_freq_t = MDTextField(
            hint_text="Frecuencia riego Tutor (días)", 
            input_filter="int", 
            opacity=0, 
            disabled=True
        )
        self.tf_fecha_t = MDTextField(
            hint_text="Último riego Tutor (AAAA-MM-DD)", 
            opacity=0, 
            disabled=True, 
            text=datetime.now().strftime('%Y-%m-%d')
        )

        # AGREGAR WIDGETS
        widgets = [
            self.img_preview, btn_img, self.tf_nombre, self.tf_especie, 
            self.tf_freq_m, self.tf_fecha_m, row_tutor, self.tf_freq_t, self.tf_fecha_t
        ]
        for w in widgets:
            self.layout_campos.add_widget(w)
            
        # --- EL TRUCO FINAL: ESPACIO SEGURO ---
        # Añadimos un widget vacío al final de 60dp de altura. 
        # Esto garantiza que el scroll siempre pueda bajar lo suficiente 
        # para mostrar el switch y los campos del tutor.
        self.layout_campos.add_widget(Widget(size_hint_y=None, height=dp(60)))
        
        self.scroll_formulario.add_widget(self.layout_campos)

        self.dialogo = MDDialog(
            title="Nueva Planta", 
            type="custom", 
            content_cls=self.scroll_formulario, 
            auto_dismiss=False,
            # ESTO EMPUJA EL DIÁLOGO HACIA ARRIBA
            pos_hint={'top': 0.95}, 
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=lambda x: self.dialogo.dismiss()),
                MDRaisedButton(text="GUARDAR", on_release=self.guardar_planta)
            ]
        )
        self.dialogo.open()

    def generar_layout_formulario(self):
        # Creamos el contenedor que se puede scrollear
        self.scroll_formulario = MDScrollView(size_hint_y=None, height=dp(400))
        self.layout_campos = MDBoxLayout(orientation="vertical", spacing=dp(12), size_hint_y=None, padding=[dp(15), dp(35), dp(15), dp(20)])
        self.layout_campos.bind(minimum_height=self.layout_campos.setter('height'))

        # Widgets del formulario
        self.img_preview = Image(source=self.imagen_seleccionada, size_hint_y=None, height=dp(100))
        btn_img = MDRaisedButton(text="ELEGIR IMAGEN", pos_hint={"center_x": 0.5}, on_release=self.mostrar_selector_imagenes)
        self.tf_nombre = MDTextField(hint_text="Nombre de la planta")
        self.tf_especie = MDTextField(hint_text="Especie")
        self.tf_freq_m = MDTextField(hint_text="Frecuencia riego Maceta (días)", input_filter="int")
        self.tf_fecha_m = MDTextField(hint_text="Último riego Maceta (AAAA-MM-DD)", text=datetime.now().strftime('%Y-%m-%d'))
        
        row_tutor = MDBoxLayout(orientation="horizontal", adaptive_height=True, padding=[0, dp(10)])
        row_tutor.add_widget(MDLabel(text="¿Tiene Tutor?", theme_text_color="Secondary"))
        self.switch_tutor = MDSwitch(active=False)
        self.switch_tutor.bind(active=self.toggle_tutor_field)
        row_tutor.add_widget(self.switch_tutor)
        
        self.tf_freq_t = MDTextField(hint_text="Frecuencia riego Tutor (días)", input_filter="int", opacity=0, disabled=True)
        self.tf_fecha_t = MDTextField(hint_text="Último riego Tutor (AAAA-MM-DD)", opacity=0, disabled=True, text=datetime.now().strftime('%Y-%m-%d'))

        for w in [self.img_preview, btn_img, self.tf_nombre, self.tf_especie, self.tf_freq_m, self.tf_fecha_m, row_tutor, self.tf_freq_t, self.tf_fecha_t]:
            self.layout_campos.add_widget(w)
        
        self.scroll_formulario.add_widget(self.layout_campos)

    def mostrar_selector_imagenes(self, *args):
        
        grid = MDGridLayout(cols=2, spacing=dp(15), adaptive_height=True, padding=dp(20))
        
        for i in range(1, 21):
            path = f"assets/img_planta_{str(i).zfill(2)}.png"
            
            # Verificamos si el archivo existe para que la app no explote
            if os.path.exists(path):
                btn = MDIconButton(
                    icon=path, 
                    icon_size=dp(100), # Tamaño grande para 2 columnas
                    on_release=lambda x, p=path: self.seleccionar_foto(p)
                )
                grid.add_widget(btn)

        self.scroll_selector = MDScrollView(size_hint_y=None, height=dp(400))
        self.scroll_selector.add_widget(grid)

        self.dialogo_selector = MDDialog(
            title="Selecciona Foto",
            type="custom",
            content_cls=self.scroll_selector,
            auto_dismiss=True
        )
        self.dialogo_selector.open()

    def seleccionar_foto(self, path):
        self.imagen_seleccionada = path
        # Actualizamos la imagen en el formulario principal
        if hasattr(self, 'img_preview'):
            self.img_preview.source = path
        # Cerramos el selector
        if hasattr(self, 'dialogo_selector'):
            self.dialogo_selector.dismiss()

    def toggle_tutor_field(self, instance, value):
        op = 1 if value else 0
        self.tf_freq_t.opacity = op
        self.tf_freq_t.disabled = not value
        self.tf_fecha_t.opacity = op
        self.tf_fecha_t.disabled = not value

    def guardar_planta(self, *args):
        data.insert_plant(
            self.tf_nombre.text if self.tf_nombre.text else "Sin nombre",
            self.tf_especie.text, "si" if self.switch_tutor.active else "no",
            int(self.tf_freq_t.text) if self.switch_tutor.active and self.tf_freq_t.text else 0,
            int(self.tf_freq_m.text) if self.tf_freq_m.text else 7,
            self.imagen_seleccionada, self.tf_fecha_m.text,
            self.tf_fecha_t.text if self.switch_tutor.active else "2026-05-12"
        )
        self.dialogo.dismiss()
        self.cargar_inventario()

    def regar_planta(self, plant_id, tipo):
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M')
        if tipo == "maceta": data.update_last_watered_m(plant_id, fecha)
        else: data.update_last_watered_t(plant_id, fecha)
        self.cargar_inventario()

    def activar_modo_eliminar(self, *args):
        self.modo_eliminar = not self.modo_eliminar
        self.renderizar_nav_bar()

    def mostrar_opciones(self, p_id):
        if self.modo_eliminar:
            self.dialogo = MDDialog(title="¿Borrar?", buttons=[
                MDFlatButton(text="NO", on_release=lambda x: self.dialogo.dismiss()),
                MDRaisedButton(text="SÍ", on_release=lambda x: (data.delete_plant(p_id), self.dialogo.dismiss(), self.cargar_inventario()))
            ])
            self.dialogo.open()

    def abrir_editor(self, planta_id):
        p = data.get_plant_by_id(planta_id)
        if not p: return

        self.planta_id_actual = planta_id 
        self.imagen_seleccionada = p[8] # image_path es el índice 8

        self.generar_layout_formulario()
        
        # Llenamos los campos con los índices correctos de la tabla
        self.img_preview.source = p[8]
        self.tf_nombre.text = str(p[1])   # name
        self.tf_especie.text = str(p[2])  # species
        self.tf_freq_m.text = str(p[5])   # irri_frequency
        self.tf_fecha_m.text = str(p[6])  # last_watered
        
        self.switch_tutor.active = True if p[3] == "si" else False
        self.tf_freq_t.text = str(p[4])   # irri_tutor
        self.tf_fecha_t.text = str(p[7])  # last_tutor_watered

        # 4. Abrimos el diálogo pero con título y botón de "ACTUALIZAR"
        self.dialogo = MDDialog(
            title="Editar Planta",
            type="custom",
            content_cls=self.scroll_formulario,
            pos_hint={'top': 0.95},
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=lambda x: self.dialogo.dismiss()),
                MDRaisedButton(text="ACTUALIZAR", on_release=self.actualizar_planta)
            ]
        )
        self.dialogo.open()

    def actualizar_planta(self, *args):
        # Tomamos los valores de los campos
        nuevo_nombre = self.tf_nombre.text
        nueva_especie = self.tf_especie.text
        tiene_tutor = "si" if self.switch_tutor.active else "no"
        f_t = int(self.tf_freq_t.text) if self.tf_freq_t.text else 0
        f_m = int(self.tf_freq_m.text) if self.tf_freq_m.text else 7
        img = self.imagen_seleccionada
        u_m = self.tf_fecha_m.text
        u_t = self.tf_fecha_t.text

        # Llamamos a la base de datos
        data.update_plant_full(self.planta_id_actual, nuevo_nombre, nueva_especie, tiene_tutor, f_t, f_m, img, u_m, u_t)
        
        self.dialogo.dismiss()
        self.cargar_inventario() # Refrescamos la pantalla