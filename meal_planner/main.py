import os
import csv
import random

from meal_planner.funcs import read_data, write_data
from meal_planner.classes import Recipe

from kivy.app import App

from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

from kivy.graphics.vertex_instructions import Rectangle, Ellipse, Line
from kivy.graphics.context_instructions import Color


# import 'properties' of different kinds (i.e., number, lists, general
# python object) that can be set in python classes, then accessed in the
# .kv file

from kivy.properties import ListProperty

def main():
    # retreive data
    initial_data = read_data('./output/recipes/')
    choice = int(input('\n\nWhat would you like to do?\n'
                        '(1) See Recipes\n'
                        '(2) Make meal plan\n'
                        '(9) Quit\n'
                        '*********'
                        '\n\n\n\nPlease enter your choice:  '
                        ))
    if choice == 1:
        print('\n' * 41)
        for r in initial_data:
            output = r.split('.')[0] + ' ' + str(initial_data[r]['is_healthy'])
            print(output)
        next = int(input('\n\nWhat next?\n'
                    '(1) Go back to main menu\n'
                    '(2) Add Recipe\n'
                    '(9) Quit\n'
                    '*********'
                    '\n\n\n\nPlease enter your choice:  '
                ))
        if next == 1:
            print('\n' * 50)
            main()
        if next == 2:
            name = input('Recipe Name:  ')
            new_recipe = Recipe(name)
            healthy = input('Is this recipe healthy (yes/no)?     ')
            if healthy == 'yes':
                new_recipe.set_health_value(True)
            new_recipe.save_self()
            main()
        elif next == 9:
            print('Good bye!')
        else:
            print('\n' * 41)
            print('***Invalid Input***\n\nReturning to main menu')
            main()
    elif choice == 2:
        days = input('How many days?      ')
        new_plan = "I'm a new plan!"
        main()
    elif choice == 9:
        print('Good bye!')
    else:
        print('\n' * 41)
        print('***Invalid Input***\n\nReturning to main menu')
        main()

class ScatterTextWidget(BoxLayout):
    # This is a kivy property, which can now be set by python
    text_color = ListProperty([1,0,0,1])

    # initialize the object to perform operations like drawing
    def __init__(self, **kwargs):
        super(ScatterTextWidget, self).__init__(**kwargs)
        # adding '.before' will build this first, pushing shapes to the
        # back. '.after' enforces being built after, putting them in the
        # the front. I.e. 'canvas.before'
        # with self.canvas:
        #     # RGBA
        #     Color(0, 1, 0, 1)
        #     # set starting position and size of objects
        #     Rectangle(pos=(0,100), size=(300, 100))
        #     Ellipse(pos=(0, 400), size=(300, 100))
        #     # give Cartesian coordinates for lines
        #     Line(points=[0, 0, 500, 600, 400, 300],
        #         close=True,
        #         width=3)

    # Set methods like any python class referenving the kivy property
    def change_label_color(self, *args):
        color = [random.random() for i in range(0,3)] + [1]
        self.text_color = color

class MealPlanner(App):
    def build(self):
        # return ScatterTextWidget() ## for a scatter-based widget
        return ScatterTextWidget()

if __name__ == '__main__':
    MealPlanner().run()
