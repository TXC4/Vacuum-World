import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, CardTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.graphics import Rectangle, Color
from kivy.uix.widget import Widget
from kivy.core.window import Window
import random

Builder.load_string('''
<EmptyWidget>:
    pos: self.pos
    size: self.size
<MyApp>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            size_hint_y: .1
            font_size: 24
            text: 'Vacuum World'
        FloatLayout:
            id: upperLevel
            orientation: 'horizontal'
            size_hint_y: .9
            BoardGrid:
                id: BG
                pos_hint: {'center_y': 0.5, 'center_x': 0.5}
                size_hint_max_x: self.height
                rows: 8
                cols: 8
                spacing: 5
            DirtyGrid:
                id: DG
                pos_hint: {'center_y': 0.5, 'center_x': 0.5}
                size_hint_max_x: self.height
                rows: 8
                cols: 8
                spacing: 5
            VacuumGrid:
                id: VG
                pos_hint: {'center_y': 0.5, 'center_x': 0.5}
                size_hint_max_x: self.height
                rows: 8
                cols: 8
                spacing: 5
''')
class EmptyWidget(Widget):
    pass

class BoardGrid(GridLayout):
    def __init__(self, **kwargs):
        super(BoardGrid, self).__init__(**kwargs)
        for i in range(64):
            self.add_widget(Image(source='carpetClean.jpg'))

globalDirt = []     
class DirtyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(DirtyGrid, self).__init__(**kwargs)
        self.dirtyPlaces = random.sample(range(64), 20)
        update = Clock.schedule_interval(self.updateGrid, 1/4)
        global globalDirt
        globalDirt = self.dirtyPlaces

    def updateGrid(self, *args):
        self.clear_widgets()
        for i in range(64):
            if i in globalDirt:
                self.add_widget(Image(source='dirt.jpg'))
            else:
                self.add_widget(EmptyWidget())

class VacuumGrid(GridLayout):
    lobby = 56
    vacPos = lobby
    stepCount = 0

    #AI Performance Measures
    cleanedRoom = 100
    stepTaken = -10
    stopOutsideLobby = -1000

    def __init__(self, **kwargs):
        super(VacuumGrid, self).__init__(**kwargs)
        for i in range(64):
            if i == self.lobby:
                self.add_widget(Image(source='vacuum.png')) 
            else:
                self.add_widget(EmptyWidget())
        #Change self.randomMovement to learn
        #Make a slider to increase and decrease speed
        update = Clock.schedule_interval(self.randomMovement, 1/4)

    def randomMovement(self, *args):
        r = random.randint(1,4)
        if r == 1:
            self.moveUp()
        elif r == 2:
            self.moveDown()
        elif r == 3:
            self.moveLeft()
        elif r == 4:
            self.moveRight()
        self.updateVacPos()

    def updateVacPos(self):    
        self.clear_widgets()
        for i in range(64):
            if i == self.vacPos:
                self.add_widget(Image(source='vacuum.png')) 
            else:
                self.add_widget(EmptyWidget())
        self.stepCount += 1
        #check if location is dirty
        global globalDirt
        for i in globalDirt:
            if self.vacPos == i:
                self.suck(i)
        print(self.stepCount, self.vacPos)

    def bumped(self):
        print("Bump")
    
    def moveLeft(self):
        if (self.vacPos % 8 == 0) or (self.vacPos == 0):
            self.bumped()
        else:
            self.vacPos -= 1

    def moveRight(self):
        #if (((self.vacPos - 1) % 8) == 0) or (self.vacPos == 63):
        if (((self.vacPos + 1) % 8) == 0):
            self.bumped()
        else:
            self.vacPos += 1

    def moveUp(self):
        if (self.vacPos < 7):
            self.bumped()
        else:
            self.vacPos -= 8

    def moveDown(self):
        if (self.vacPos > 55):
            self.bumped()
        else:
            self.vacPos += 8

    def suck(self, loc):
        global globalDirt
        globalDirt.remove(loc)
        print("Suck")
        
class MyApp(App, BoxLayout):
    def build(self):
        return self

if __name__ == '__main__':
    MyApp().run()