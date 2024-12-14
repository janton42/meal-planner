import os
import json
import csv

from meal_planner.funcs import read_data, write_data, shuffle

class RealThing:
    def __init__(self, name):
        self.name = name
        self.output_path = './output/'
        self.subpath = ''
        self.filename = ''

    def set_subpath(self, subpath):
        self.subpath = subpath
        return self.subpath

    def set_filename(self, filename):
        self.filename = filename
        return self.filename

    def save_self(self):
        if self.subpath == '':
            raise ValueError('Subpath not set.')
        elif self.filename == '':
            raise ValueError('Filename not set.')
        self.filename += '.json'
        save_path = os.path.join(self.output_path, self.subpath, self.filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        data = self.__dict__
        write_data(data, save_path)

        confirmation = f'{self.name} saved to {self.subpath}.'
        return confirmation
class Ingredient(RealThing):
    """docstring for Ingredient."""

    def __init__(self, name):
        super().__init__(name)
        self.state = ''
        self.measures = list()
        self.expiration = ''
        self.location = ''

    # Create operations for the Ingredient class
    def set_state(self, state: str):
        if state == self.state:
            print(f'State is already set to "{self.state}".')
            return f'State is already set to "{self.state}".'
        else:
            self.state = state
            print(f'State has been set to "{self.state}".')
            return f'State has been set to "{self.state}".'

    def add_measure(self, measure: dict):
        self.measures.append(measure)
        print(f'{measure["quantity"]} of {self.name} added to measures list.')

    def set_expiration(self, expiration: str):
        if expiration == self.expiration:
            print(f'Expiration is already set to "{self.expiration}".')
            return f'Expiration is already set to "{self.expiration}".'
        else:
            self.expiration = expiration
            print(f'Expiration has been set to "{self.expiration}".')
            return f'Expiration has been set to "{self.expiration}".'

    def set_location(self, location: str):
        if location == self.location:
            print(f'Location is already set to "{self.location}".')
            return f'Location is already set to "{self.location}".'
        else:
            self.location = location
            print(f'Location has been set to "{self.location}".')
            return f'Location has been set to "{self.location}".'


    # Read operations for the Ingredient class
    def get_measures(self):
        return self.measures

    def get_state(self):
        return self.state

    def get_expiration(self):
        return self.expiration

    # Delete operations for the Ingredient class

    def remove_measure(self, measure: dict):
        if measure in self.measures:
            self.measures.remove(measure)
            print(f'{measure["quantity"]} of {self.name} removed from measures list.')
        else:
            print(f'{measure["quantity"]} of {self.name} not found in measures list.')



    def __str__(self):
        return self.name



class Recipe(RealThing):
    """docstring for Recipe."""

    def __init__(self, name):
        super().__init__(name)
        self.ingredients = list()
        self.directions = ''
        self.is_healthy = False

    # Create operations for the Recipe class
    def add_ingredients(self, ingredients: list):
        for i in ingredients:
            self.ingredients.append(i)
            print(f'{i["name"]} added to {self.name} ingredients list')

    def add_directions(self, directions: str):
        self.directions = directions
        print(f'Directions added to {self.name}.')

    def set_health_value(self, healthy: bool):
        if healthy == self.is_healthy:
            print(f'"is_healthy" is already set to "{self.is_healthy}".')
            return f'"is_healthy" is already set to "{self.is_healthy}".'
        else:
            self.is_healthy = healthy
            print(f'"is_healthy" has been set to "{self.is_healthy}".')
            return f'"is_healthy" has been set to "{self.is_healthy}".'

    # Read operations for the Recipe class
    def get_ingredients(self):
        return self.ingredients

    def get_directions(self):
        return self.directions

    def get_health_value(self):
        return self.is_healthy

    # Delete operations for the Recipe class
    def remove_ingredient(self, ingredient: dict):
        if ingredient in self.ingredients:
            self.ingredients.remove(ingredient)
            print(f'{ingredient["name"]} removed from {self.name} ingredients list.')
        else:
            print(f'{ingredient["name"]} not found in {self.name} ingredients list.')


class Storage(RealThing):
    """docstring for Storage."""

    def __init__(self, name):
        super().__init__(name)
        self.contents = dict()

    # Create operations for the Storage class
    def add_item(self, item: RealThing):
        if item.name not in self.contents:
            self.contents[item.name] = 1
        else:
            self.contents[item.name] += 1
        print(f'There are {self.contents[item.name]} {item.name} in {self.name}.')

    # Read operations for the Storage class
    def get_contents(self):
        return self.contents

    # Delete operations for the Storage class
    def remove_item(self, item: RealThing):
        if self.contents[item.name] > 0:
            self.contents[item.name] -= 1
            print(f'There are {self.contents[item.name]} {item.name} in {self.name}.')
        else:
            print(f'There are no {item.name} in {self.name}.')

class MealPlan(object):
    """docstring for MealPlan."""

    def __init__(self, recipes, days):
        super(MealPlan, self).__init__()
        self.all_recipes = recipes
        self.fatty_recipes = list()
        self.healthy_recipes = list()
        self.days = int(days)
        self.healthy_meals = 80
        self.fatty_gap = 3

    def split_recipes(self):
        for recipe in self.all_recipes:
            if self.all_recipes[recipe]['is_healthy'] == True:
                self.healthy_recipes.append(recipe)
            else:
                self.fatty_recipes.append(recipe)
        self.healthy_recipes = shuffle(self.healthy_recipes)
        self.fatty_recipes = shuffle(self.fatty_recipes)

    def make_plan(self):
        self.split_recipes()
        meal_plan = list()
        fr_use_count = 0
        hr_use_count = 0
        while self.days > 0:
            if self.days % 3 == 0:
                meal = self.fatty_recipes[fr_use_count].split('.')[0]
                meal_plan.insert(0, meal)
                fr_use_count += 1
            else:
                if hr_use_count == len(self.healthy_recipes):
                    self.healthy_recipes = shuffle(self.healthy_recipes)
                    hr_use_count = 0
                meal = self.healthy_recipes[hr_use_count].split('.')[0]
                meal_plan.insert(0, meal)
                hr_use_count += 1
            self.days -= 1
        for meal in meal_plan:
            print(meal)
        return meal_plan
