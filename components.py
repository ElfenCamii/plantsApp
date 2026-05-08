from kivymd.uix.card import MDCard
from kivy.clock import Clock

class LongPressCard(MDCard):
    __events__ = ('on_long_press',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.long_press_time = 1.0  
        self._clock_ev = None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._clock_ev = Clock.schedule_once(self._trigger_long_press, self.long_press_time)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self._clock_ev:
            Clock.unschedule(self._clock_ev)
        return super().on_touch_up(touch)

    def _trigger_long_press(self, dt):
        self.dispatch('on_long_press')

    def on_long_press(MDCard):
        pass