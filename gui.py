from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton, MDRectangleFlatIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDSwitch

from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.properties import NumericProperty, ColorProperty, StringProperty
from kivy.metrics import dp

import data
import functions
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
            Color(0.8, 0.8, 0.8, 0.3)
            Line(circle=(cx, cy, radius), width=dp(2))
            Color(*self.color)
            angle_start = 90
            angle_end = 90 - (max(0.1, self.value) / 100) * 360
            Line(circle=(cx, cy, radius, angle_end, angle_start), width=dp(3.5), cap='round')

class RegandoAndo(MDApp):
    dialogo = None 
    dialogo_selector = None
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
        return self.root

    def renderizar_nav_bar(self):
        self.nav_bar.clear_widgets()
        color_iconos = [1, 0.3, 0.3, 1] if self.modo_eliminar else [1, 1, 1, 1]
        items = [("trash-can", self.activar_modo_eliminar), ("plus-circle", self.abrir_formulario), ("cog", self.abrir_ajustes)]
        for icon, func in items:
            area = MDFloatLayout(size_hint_x=0.33)
            btn = MDIconButton(icon=icon, theme_text_color="Custom", text_color=color_iconos,
                               pos_hint={'center_x': 0.5, 'center_y': 0.5}, on_release=func)
            if icon == "plus-circle": btn.icon_size = dp(36)
            area.add_widget(btn)
            self.nav_bar.add_widget(area)

    def cargar_inventario(self):
        self.contenedor_grid.clear_widgets()
        plantas = data.get_all_plants()
        for p in plantas:
            porc_m = data.calcular_barra_vida(p[6], p[5])
            tarjeta = LongPressCard(orientation='vertical', padding=dp(10), size_hint=(1, None), height=dp(250), radius=[dp(20)], elevation=2)
            tarjeta.bind(on_release=lambda x, p_id=p[0]: self.mostrar_opciones(p_id))
            
            tarjeta.add_widget(MDLabel(text=f"[b]{p[1]}[/b]", markup=True, halign="center", font_style="H6", size_hint_y=None, height=dp(30)))
            tarjeta.add_widget(MDLabel(text=p[2] if p[2] else " ", halign="center", font_style="Subtitle2", theme_text_color="Secondary", size_hint_y=None, height=dp(20)))
            tarjeta.add_widget(Image(source=p[8], size_hint=(1, None), height=dp(80), fit_mode="contain"))
            
            layout_riego = MDBoxLayout(orientation="horizontal", spacing=dp(20), adaptive_size=True, pos_hint={"center_x": 0.5})
            area_m = MDAnchorLayout(size_hint=(None, None), size=(dp(50), dp(50)))
            area_m.add_widget(CircularProgress(value=porc_m, color=[0.2, 0.7, 0.3, 1], size=(dp(46), dp(46))))
            area_m.add_widget(MDIconButton(icon="", on_release=lambda x, p_id=p[0]: self.regar_planta(p_id, "maceta")))
            area_m.add_widget(MDLabel(text="M", font_style="Caption", halign="center"))
            layout_riego.add_widget(area_m)

            if str(p[3]).lower() == "si":
                porc_t = data.calcular_barra_vida(p[7], p[4])
                area_t = MDAnchorLayout(size_hint=(None, None), size=(dp(50), dp(50)))
                area_t.add_widget(CircularProgress(value=porc_t, color=[0.6, 0.4, 0.2, 1], size=(dp(46), dp(46))))
                area_t.add_widget(MDIconButton(icon="", on_release=lambda x, p_id=p[0]: self.regar_planta(p_id, "tutor")))
                area_t.add_widget(MDLabel(text="T", font_style="Caption", halign="center"))
                layout_riego.add_widget(area_t)

            tarjeta.add_widget(layout_riego)
            self.contenedor_grid.add_widget(tarjeta)

    # --- NUEVO SELECTOR DE IMÁGENES TIPO GRID ---
    def mostrar_selector_imagenes(self, *args):
        # Crear la cuadrícula de imágenes
        lista_imagenes = [f"assets/img_planta_0{i}.png" for i in range(1, 10)]
        grid_fotos = MDGridLayout(cols=3, spacing=dp(10), adaptive_height=True, padding=dp(10))
        
        for img_path in lista_imagenes:
            btn_foto = MDIconButton(
                icon=img_path,
                icon_size=dp(70),
                size_hint=(None, None),
                size=(dp(80), dp(80))
            )
            # Al seleccionar, actualizamos la imagen y cerramos SOLO el selector
            btn_foto.bind(on_release=lambda x, path=img_path: self.seleccionar_esta_imagen(path))
            grid_fotos.add_widget(btn_foto)

        # Usar un Box con Scroll para que el contenido no rompa el diálogo
        contenido = MDBoxLayout(orientation="vertical", size_hint_y=None, height=dp(300))
        scroll = MDScrollView()
        scroll.add_widget(grid_fotos)
        contenido.add_widget(scroll)

        self.dialogo_selector = MDDialog(
            title="Selecciona una Planta",
            type="custom",
            content_cls=contenido,
        )
        self.dialogo_selector.open()

    def seleccionar_esta_imagen(self, path):
        self.imagen_seleccionada = path
        # Actualizamos la fuente de la imagen en el formulario anterior
        self.img_preview.source = path 
        self.dialogo_selector.dismiss()

    def abrir_formulario(self, *args):
        self.imagen_seleccionada = "assets/img_planta_01.png"
        layout = MDBoxLayout(orientation="vertical", spacing=dp(10), size_hint_y=None, height=dp(480), padding=dp(10))
        
        self.tf_nombre = MDTextField(hint_text="Nombre de la planta")
        self.tf_especie = MDTextField(hint_text="Especie")
        self.tf_freq_m = MDTextField(hint_text="Frecuencia Maceta (días)", input_filter="int")
        
        row_tutor = MDBoxLayout(orientation="horizontal", adaptive_height=True)
        row_tutor.add_widget(MDLabel(text="¿Tiene Tutor?", theme_text_color="Secondary"))
        self.switch_tutor = MDSwitch(active=False)
        self.switch_tutor.bind(active=self.toggle_tutor_field)
        row_tutor.add_widget(self.switch_tutor)
        
        self.tf_freq_t = MDTextField(hint_text="Frecuencia Tutor (días)", input_filter="int", opacity=0, disabled=True)
        
        self.img_preview = Image(source=self.imagen_seleccionada, size_hint_y=None, height=dp(80))
        btn_abrir_grid = MDRaisedButton(
            text="CAMBIAR IMAGEN", 
            pos_hint={"center_x": 0.5},
            on_release=self.mostrar_selector_imagenes # Aquí llamamos al selector
        )

        layout.add_widget(self.tf_nombre)
        layout.add_widget(self.tf_especie)
        layout.add_widget(self.tf_freq_m)
        layout.add_widget(row_tutor)
        layout.add_widget(self.tf_freq_t)
        layout.add_widget(self.img_preview)
        layout.add_widget(btn_abrir_grid)

        # IMPORTANTE: auto_dismiss=False para que no se cierre al abrir otro diálogo
        self.dialogo = MDDialog(
            title="Nueva Planta",
            type="custom",
            content_cls=layout,
            auto_dismiss=False, 
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=lambda x: self.dialogo.dismiss()),
                MDRaisedButton(text="GUARDAR", on_release=self.guardar_planta)
            ]
        )
        self.dialogo.open()

    def toggle_tutor_field(self, instance, value):
        self.tf_freq_t.opacity = 1 if value else 0
        self.tf_freq_t.disabled = not value

    def guardar_planta(self, *args):
        tutor_status = "si" if self.switch_tutor.active else "no"
        f_t = int(self.tf_freq_t.text) if self.switch_tutor.active and self.tf_freq_t.text else 0
        f_m = int(self.tf_freq_m.text) if self.tf_freq_m.text else 7
        data.insert_plant(self.tf_nombre.text, self.tf_especie.text, tutor_status, f_t, f_m, self.imagen_seleccionada)
        self.dialogo.dismiss()
        self.cargar_inventario()

    def regar_planta(self, plant_id, tipo):
        fecha = datetime.now().strftime('%Y-%m-%d')
        if tipo == "maceta": data.update_last_watered_m(plant_id, fecha)
        else: data.update_last_watered_t(plant_id, fecha)
        self.cargar_inventario()

    def activar_modo_eliminar(self, *args):
        self.modo_eliminar = not self.modo_eliminar
        self.renderizar_nav_bar()

    def mostrar_opciones(self, plant_id):
        if self.modo_eliminar:
            self.dialogo = MDDialog(
                title="¿Eliminar planta?",
                buttons=[
                    MDFlatButton(text="NO", on_release=lambda x: self.dialogo.dismiss()),
                    MDRaisedButton(text="SÍ, ELIMINAR", on_release=lambda x: self.confirmar_borrado(plant_id))
                ]
            )
            self.dialogo.open()

    def confirmar_borrado(self, plant_id):
        data.delete_plant(plant_id)
        self.dialogo.dismiss()
        self.cargar_inventario()

    def abrir_ajustes(self, *args): pass

if __name__ == "__main__":
    RegandoAndo().run()