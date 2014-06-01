import kivy
kivy.require('1.7.2')

import random

from kivy.lang import Builder
from kivy.app import App
from kivy.properties import ListProperty
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Ellipse, Line, Rectangle


class Painter(Widget):

    #color = (0., 1., 0.4)

    def __init__(self, **kwargs):
        super(Painter, self).__init__(**kwargs)
        self.color = (random.random(), 1., 1.)

    def on_touch_down(self, evt):

        if not self.collide_point(evt.x, evt.y):
            return

        with self.canvas:
            Color(*self.color, mode = "hsv")
            d = 10
            evt.ud["trace"] = Line(point=(evt.x, evt.y), width=5)
            evt.ud["owner"] = id(self)

    def on_touch_move(self, evt):
        if not self.collide_point(evt.x, evt.y):
            return

        if "owner" in evt.ud and evt.ud["owner"] == id(self):
            evt.ud["trace"].points += (evt.x, evt.y)

    def draw_background(self, arg1 = None, arg2 = None):

        with self.canvas:
            Color(1, 1, 1, 0.5)
            Rectangle(pos= self.pos, size= self.size)


    def clear_letter(self):
        self.canvas.clear()
        self.draw_background()

class LettersApp(App):

    def next_word(self):
        print("Next word!")

if __name__ == "__main__":
    LettersApp().run()
