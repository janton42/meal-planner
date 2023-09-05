import os
import json
import csv

from funcs import read_data, write_data, shuffle

class Recipe(object):
    """docstring for Recipe."""

    def __init__(self, name):
        super(Recipe, self).__init__()
        self.name = name
        self.ingredients = list()
        self.output_path = './meal_planner/output/'
        self.directions = ''
        self.is_healthy = False

    def list_ingredients(self):
        return self.ingredients

    def add_ingredients(self, ingredients: list):
        for i in ingredients:
            self.ingredients.append(i)
            print(f'{i["name"]} added to {self.name} ingredients list')

    def export_ingredients(self):
        write_data(
                data = self.ingredients,
                path = self.output_path + self.name + '_ingredients_export.json'
            )
        print(f'Ingredient list for {self.name} exported')
        return f'Ingredient list for {self.name} exported'

    def set_health_value(self, healthy: bool):
        if healthy == self.is_healthy:
            print(f'"is_healthy" is already set to "{self.is_healthy}".')
            return f'"is_healthy" is already set to "{self.is_healthy}".'
        else:
            self.is_healthy = healthy
            print(f'"is_healthy" has been set to "{self.is_healthy}".')
            return f'"is_healthy" has been set to "{self.is_healthy}".'

    def save_self(self):
        filename = self.name + '.json'
        write_data(
                data = {
                    'name': self.name,
                    'ingredients': self.ingredients,
                    'directions': self.directions,
                    'is_healthy': self.is_healthy,
                },
                path = self.output_path + 'recipes/' + filename
            )
        print(f'{self.name} saved to Recipes.')
        return f'{self.name} saved to Recipes.'

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
                if fr_use_count == len(self.fatty_recipes):
                    self.fatty_recipes = shuffle(self.fatty_recipes)
                    fr_use_count = 0
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
