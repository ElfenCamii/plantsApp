# from kivy.config import Config
# Config.set('graphics', 'width', '412')
# Config.set('graphics', 'height', '915')
# Config.set('graphics', 'resizable', False)

# from kivymd.app import MDApp
# from kivymd.uix.screen import MDScreen
# from kivymd.uix.scrollview import MDScrollView
# from kivymd.uix.gridlayout import MDGridLayout
# from kivymd.uix.floatlayout import MDFloatLayout
# from kivymd.uix.button import MDFloatingActionButton, MDRaisedButton, MDFlatButton, MDIconButton, MDFloatingActionButtonSpeedDial                      
# from kivymd.uix.card import MDCard
# from kivymd.uix.label import MDLabel
# from kivymd.uix.progressbar import MDProgressBar
# from kivymd.uix.dialog import MDDialog
# from kivymd.uix.textfield import MDTextField
# from kivymd.uix.selectioncontrol import MDSwitch
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.image import Image
# from kivy.metrics import dp
# from kivy.core.window import Window
# from kivymd.uix.boxlayout import MDBoxLayout
# from kivy.clock import Clock

# import data
# import functions

# Window.top = 40
# Window.left = 500

# # --- Clase personalizada para detectar el toque largo ---
# class LongPressCard(MDCard):
#     __events__ = ('on_long_press',)

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.long_press_time = 1.0  
#         self._clock_ev = None

#     def on_touch_down(self, touch):
#         if self.collide_point(*touch.pos):
#             self._clock_ev = Clock.schedule_once(self._trigger_long_press, self.long_press_time)
#         return super().on_touch_down(touch)

#     def on_touch_up(self, touch):
#         if self._clock_ev:
#             Clock.unschedule(self._clock_ev)
#         return super().on_touch_up(touch)

#     def _trigger_long_press(self, dt):
#         self.dispatch('on_long_press')

#     def on_long_press(self, *args):
#         pass 

# # --- Clase Principal RegandoAndo ---
# class RegandoAndo(MDApp):
#     dialogo = None 
#     dialogo_eliminar = None
#     imagen_seleccionada = "assets/img_planta_01.png"
#     lista_botones_iconos = []

#     def build(self):
#         data.init_db() 
#         self.theme_cls.primary_palette = "Green"
#         self.theme_cls.theme_style = "Light"
        
#         self.pantalla_principal = MDScreen()
#         layout_base = MDFloatLayout()

#         scroll = MDScrollView(size_hint=(1, 1))
#         self.contenedor_grid = MDGridLayout(
#             cols=2, spacing=dp(12), padding=dp(12), adaptive_height=True 
#         )

#         self.cargar_inventario()

#         boton_agregar = MDFloatingActionButton(
#             icon="plus",
#             md_bg_color=self.theme_cls.primary_color,
#             pos_hint={'center_x': 0.85, 'center_y': 0.08},
#             on_release=self.abrir_formulario 
#         )

#         scroll.add_widget(self.contenedor_grid)
#         layout_base.add_widget(scroll)
#         layout_base.add_widget(boton_agregar)
        
#         self.pantalla_principal.add_widget(layout_base)
#         return self.pantalla_principal

#     def abrir_formulario(self, *args):
#         self.lista_botones_iconos = []
#         scroll = MDScrollView(size_hint_y=None, height=dp(450))
        
#         self.contenido = BoxLayout(
#             orientation="vertical", 
#             spacing="20dp", 
#             padding=[dp(20), dp(20), dp(20), dp(20)], 
#             size_hint_y=None
#         )
#         self.contenido.bind(minimum_height=self.contenido.setter('height'))

#         self.campo_nombre = MDTextField(hint_text="Nombre de la planta", mode="rectangle")
#         self.campo_especie = MDTextField(hint_text="Especie", mode="rectangle")
#         self.campo_frec_m = MDTextField(hint_text="Riego Maceta (días)", text="7", input_filter="int", mode="rectangle")
        
#         fila_tutor = BoxLayout(
#             orientation="horizontal", 
#             size_hint_y=None, 
#             height="48dp",
#             padding=[0, 0, dp(15), 0]
#         )
#         fila_tutor.add_widget(MDLabel(text="¿Tiene tutor?", theme_text_color="Secondary"))
        
#         self.switch_tutor = MDSwitch(
#             active=False, 
#             pos_hint={'center_y': 0.5},
#             size_hint=(None, None), 
#             size=(dp(48), dp(32))
#         )
#         self.switch_tutor.bind(active=self.mostrar_campo_tutor)
#         fila_tutor.add_widget(self.switch_tutor)
        
#         self.campo_frec_t = MDTextField(
#             hint_text="Riego Tutor (días)", text="15", 
#             input_filter="int", mode="rectangle",
#             size_hint_y=None, height=0, opacity=0
#         )
        
#         label_selector = MDLabel(text="Selecciona un icono:", font_style="Caption", theme_text_color="Secondary")
#         selector_grid = MDGridLayout(cols=3, spacing="15dp", adaptive_height=True)
        
#         for i in range(1, 10):
#             nombre_img = f"assets/img_planta_0{i}.png"
#             btn_img = MDIconButton(
#                 icon=nombre_img, icon_size=dp(40),
#                 on_release=lambda x, path=nombre_img: self.seleccionar_icono(path, x)
#             )
#             self.lista_botones_iconos.append(btn_img)
#             selector_grid.add_widget(btn_img)

#         self.contenido.add_widget(self.campo_nombre)
#         self.contenido.add_widget(self.campo_especie)
#         self.contenido.add_widget(self.campo_frec_m)
#         self.contenido.add_widget(fila_tutor)
#         self.contenido.add_widget(self.campo_frec_t)
#         self.contenido.add_widget(label_selector)
#         self.contenido.add_widget(selector_grid)

#         scroll.add_widget(self.contenido)

#         self.dialogo = MDDialog(
#             title="Nueva Planta",
#             type="custom",
#             content_cls=scroll,
#             buttons=[
#                 MDFlatButton(text="CANCELAR", on_release=lambda x: self.dialogo.dismiss()),
#                 MDRaisedButton(text="GUARDAR", md_bg_color=self.theme_cls.primary_color, on_release=self.guardar_nueva_planta)
#             ],
#         )
#         self.dialogo.open()

#     def mostrar_campo_tutor(self, instance, value):
#         if value:
#             self.campo_frec_t.height = dp(60)
#             self.campo_frec_t.opacity = 1
#             self.campo_frec_t.size_hint_y = None
#         else:
#             self.campo_frec_t.height = 0
#             self.campo_frec_t.opacity = 0
#             self.campo_frec_t.size_hint_y = None

#     def seleccionar_icono(self, ruta, instancia):
#         self.imagen_seleccionada = ruta
#         for btn in self.lista_botones_iconos:
#             btn.md_bg_color = [0, 0, 0, 0]
#         instancia.md_bg_color = self.theme_cls.primary_light

#     def guardar_nueva_planta(self, *args):
#         nombre = self.campo_nombre.text
#         especie = self.campo_especie.text
#         tutor = "si" if self.switch_tutor.active else "no"
#         frec_m = int(self.campo_frec_m.text) if self.campo_frec_m.text.isdigit() else 7
#         frec_t = int(self.campo_frec_t.text) if (tutor == "si" and self.campo_frec_t.text.isdigit()) else 0
        
#         data.insert_plant(nombre, especie, tutor, frec_t, frec_m, self.imagen_seleccionada)
#         self.dialogo.dismiss()
#         self.cargar_inventario()

#     # --- NUEVAS FUNCIONES PARA ELIMINAR ---
#     def mostrar_opciones(self, plant_id):
#         self.dialogo_eliminar = MDDialog(
#             title="¿Eliminar planta?",
#             text="Esta acción no se puede deshacer.",
#             buttons=[
#                 MDFlatButton(text="CANCELAR", on_release=lambda x: self.dialogo_eliminar.dismiss()),
#                 MDRaisedButton(
#                     text="ELIMINAR", 
#                     md_bg_color=(1, 0, 0, 1), # Rojo
#                     on_release=lambda x: self.confirmar_eliminacion(plant_id)
#                 ),
#             ],
#         )
#         self.dialogo_eliminar.open()

#     def confirmar_eliminacion(self, plant_id):
#         data.delete_plant(plant_id) # Llama a tu función en data.py
#         self.dialogo_eliminar.dismiss()
#         self.cargar_inventario()

#     def cargar_inventario(self):
#         self.contenedor_grid.clear_widgets()
#         plantas = data.get_all_plants()

#         for p in plantas:
#             tiene_tutor = str(p[3]).lower() == "si"
#             porcentaje_m = functions.obtener_estado_riego(p[6], p[5])
            
#             # CAMBIO: Usamos LongPressCard en lugar de MDCard
#             tarjeta = LongPressCard(
#                 orientation='vertical', 
#                 padding=[dp(10), dp(5), dp(10), dp(10)],
#                 spacing=dp(5), 
#                 size_hint=(None, None), 
#                 width=dp(180),
#                 height=dp(180),
#                 radius=[dp(20)], 
#                 elevation=2
#             )
#             # Vinculamos el evento de toque largo
#             tarjeta.bind(on_long_press=lambda instance, plant_id=p[0]: self.mostrar_opciones(plant_id))

#             contenedor_titulos = MDBoxLayout(orientation="vertical", adaptive_height=True, spacing=0)
#             contenedor_titulos.add_widget(MDLabel(
#                 text=f"[b]{p[1]}[/b]", markup=True, halign="center", 
#                 font_style="H6", adaptive_height=True
#             ))
#             contenedor_titulos.add_widget(MDLabel(
#                 text=p[2], halign="center", 
#                 font_style="Subtitle1", theme_text_color="Secondary", 
#                 adaptive_height=True
#             ))
#             tarjeta.add_widget(contenedor_titulos)
            
#             tarjeta.add_widget(Image(
#                 source=p[8], 
#                 size_hint=(1, None), 
#                 height=dp(60), 
#                 allow_stretch=True
#             ))

#             layout_barras = MDBoxLayout(orientation="vertical", spacing=dp(2), adaptive_height=True)

#             # Maceta
#             layout_barras.add_widget(MDProgressBar(
#                 value=porcentaje_m, size_hint_x=0.9, pos_hint={"center_x": 0.5}, height=dp(4), size_hint_y=None
#             ))
#             layout_barras.add_widget(MDLabel(
#                 text=f"M: {porcentaje_m}%", font_style="Caption", halign="center", adaptive_height=True
#             ))

#             # Tutor
#             if tiene_tutor:
#                 porcen_t = functions.obtener_estado_riego(p[7], p[4])
#                 color_barra, texto_tutor, valor_barra = (0.6, 0.4, 0.2, 1), f"T: {porcen_t}%", porcen_t
#             else:
#                 color_barra, texto_tutor, valor_barra = (0.8, 0.8, 0.8, 1), "T: No", 100

#             layout_barras.add_widget(MDProgressBar(
#                 value=valor_barra, color=color_barra, size_hint_x=0.9, 
#                 pos_hint={"center_x": 0.5}, height=dp(4), size_hint_y=None
#             ))
#             layout_barras.add_widget(MDLabel(
#                 text=texto_tutor, font_style="Caption", halign="center", adaptive_height=True
#             ))
            
#             tarjeta.add_widget(layout_barras)
#             self.contenedor_grid.add_widget(tarjeta)

# if __name__ == "__main__":
#     RegandoAndo().run()