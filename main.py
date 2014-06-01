import kivy
kivy.require('1.7.2')

import random

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Ellipse, Line


class Painter(Widget):

    color = (0., 1., 0.4)
    def on_touch_down(self, evt):
        #global color
        #color = (random.random(), 1., 1.)
        with self.canvas:
            Color(*Painter.color)
            d = 10
            evt.ud["trace"] = Line(point=(evt.x, evt.y), width=5)

    def on_touch_move(self, evt):
        evt.ud["trace"].points += (evt.x, evt.y)


class MultiPaintApp(App):

    def build(self):
        global color

        top = Widget()
        painter = Painter()
        clearBtn = Button(text="Clear !")
        whiteBtn = Button(background_color = [1,1,1,1]) #, size=(150,150), size_hint=(.3, 1))
        redBtn = Button(background_color = [1,0,0,1]) #, size=(150,150), size_hint=(.3, 1))
        greenBtn = Button(background_color = [0,1,0,1]) #, size=(150,150), size_hint=(.3, 1))

        top.add_widget(painter)
        
        layout = BoxLayout(orientation='vertical', size=(100, 400), spacing = 10)
        layout.add_widget(whiteBtn)
        layout.add_widget(greenBtn)
        layout.add_widget(redBtn)
        layout.add_widget(clearBtn)
        top.add_widget(layout)

        def set_white(obj):
            Painter.color = (1., 1., 0.7)


        def set_green(obj):
            Painter.color = (0., 1., 0.4)

        def set_red(obj):
            Painter.color = (1., 0., 0.)

        def clear_canvas(obj):
            painter.canvas.clear()

        clearBtn.bind(on_release=clear_canvas)
        redBtn.bind(on_release=set_red)
        greenBtn.bind(on_release=set_green)
        whiteBtn.bind(on_release=set_white)

        return top

if __name__ == "__main__":
    MultiPaintApp().run()
