import kivy
kivy.require('1.7.2')

import random
import os
import time, datetime 
import hashlib

from kivy.lang import Builder
from kivy.app import App
from kivy.properties import ListProperty
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.logger import Logger
import logging
Logger.setLevel(logging.DEBUG)

app = None


class Painter(Widget):

    #color = (0., 1., 0.4)

    def __init__(self, **kwargs):
        super(Painter, self).__init__(**kwargs)
        self.color = (random.random(), 1., 1.)
        self.line = None
        self.starttime = None
        self.timing = None

    def on_touch_down(self, evt):

        if not self.collide_point(evt.x, evt.y):
            return

        with self.canvas:
            Color(*self.color, mode = "hsv")
            d = 10
            self.line = Line(points=(evt.x, evt.y), width=3)
            self.starttime = time.time()
            self.timing = [0]
            evt.ud["owner"] = self

    def on_touch_up(self, evt):

        if not self.collide_point(evt.x, evt.y):
            return

        self.save()

    def on_touch_move(self, evt):
        if not self.collide_point(evt.x, evt.y):
            return

        if "owner" in evt.ud and evt.ud["owner"] == self:
            self.line.points += (evt.x, evt.y)
            self.timing.append(int((time.time() - self.starttime) * 1000))

    def draw_background(self, arg1 = None, arg2 = None):

        with self.canvas:
            Color(1, 1, 1, 0.5)
            Rectangle(pos= (self.x + self.width * 0.1, self.y + self.height * 0.1),
                      size = (self.width * 0.8, self.height * 0.8))



    def save(self):
        letter, word, age = self.letter, app.current_word, app.get_age()

        filename = "%s-%d-%s" % (letter, age, hashlib.sha1(str(id(self)) + str(datetime.datetime.now())).hexdigest()[:6])

        fullpath = os.path.join(app.user_data_dir, filename)

        Logger.info("Saving letter %s to %s" % (letter, fullpath))
        with open(fullpath, 'w') as data:
                data.write("# letter %s\n" % letter)
                data.write("# date: %s\n" % datetime.datetime.now())
                data.write("# word: %s, age: %s\n" % (word, age))
                data.write("# timestamp (ms) --- x (px) --- y (px)\n")
                for i, t in enumerate(self.timing):
                    data.write("%d\t%.2f\t%.2f\n" % (t, 
                                self.line.points[2 * i] - self.x,
                                self.line.points[2 * i + 1] - self.y))


    def clear_letter(self):
        self.save()
        self.color = (random.random(), 1., 1.)
        self.canvas.clear()
        self.draw_background()

class WordButton(Button):
    pass

class LetterBox(BoxLayout):
    pass

class DrawScreen(Screen):
    
    def setword(self, word, file):

        self.ids.current_letter.source = file

        self.ids.letters_container.clear_widgets()
        for i in range(len(word)):
            letterbox = LetterBox()
            letterbox.ids.letter_painter.letter = word[i]
            self.ids.letters_container.add_widget(letterbox)

class SelectScreen(Screen):

    def __init__(self, **kwargs):
        super(SelectScreen, self).__init__(**kwargs)

        words = {os.path.basename(f)[:-4]: "words/" + f for f in os.listdir('words/') if f.endswith("png")}

        for n, f in words.items():
            Logger.info("Adding word %s (%s)" % (n,f))
            btn = WordButton()
            btn.source = f
            btn.name = n
            btn.width = btn.height * btn.ids.image.image_ratio
            self.ids.gridofwords.add_widget(btn)


class IdScreen(Screen):
    pass


class LettersApp(App):

    def __init__(self, **kwargs):
        super(LettersApp, self).__init__(**kwargs)

        if not os.path.exists(self.user_data_dir):
            os.makedirs(self.user_data_dir)

        self.current_word = None

    def build(self):
        self.sm = ScreenManager()

        self.idscreen = IdScreen(name="id")
        self.sm.add_widget(self.idscreen)

        self.sm.add_widget(SelectScreen(name="select"))
        
        self.drawscreen = DrawScreen(name="draw")
        self.sm.add_widget(self.drawscreen)

        self.sm.current = "id"

        return self.sm

    def get_age(self):
        return int(self.idscreen.ids.age.value)


    def switchto(self, btn):

        word, file = btn.name, btn.source
        Logger.info("Switching to %s (%s)" % (word, file))
        self.current_word = word
        self.drawscreen.setword(word, file)
        self.sm.current = 'draw'

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == "__main__":
    app = LettersApp()
    app.run()
