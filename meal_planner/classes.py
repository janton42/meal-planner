import os

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
        self.filename = filename + '.json'
        return self.filename

    def save_self(self):
        if self.subpath == '':
            raise ValueError('Subpath not set.')
        elif self.filename == '':
            raise ValueError('Filename not set.')
        save_path = os.path.join(self.output_path, self.subpath, self.filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        data = self.__dict__
        write_data(data, save_path)

        confirmation = f'{self.name} saved to {self.subpath}.'
        return confirmation

    def __str__(self):
        return self.name


class Ingredient(RealThing):
    """docstring for Ingredient."""

    def __init__(self, name, **kwargs):
        super().__init__(name)
        self.subpath = 'ingredients'
        self.filename = name + '.json'
        self.state = kwargs.get('state', '')
        self.measures = kwargs.get('measures', list())
        self.expiration = kwargs.get('expiration', '')
        self.location = kwargs.get('location', '')

    # Create operations for the Ingredient class
    def set_state(self, state: str):
        if state == self.state:
            print(f'State is already set to "{self.state}".')
            return f'State is already set to "{self.state}".'
        else:
            self.state = state
            print(f'State has been set to "{self.state}".')
            return f'State has been set to "{self.state}".'

    def add_measure(self, measure: str):
        if measure in self.measures:
            print(f'{measure} of {self.name} already in measures list.')
            return f'{measure} of {self.name} already in measures list.'
        else:
            self.measures.append(measure)
            print(f'{measure} of {self.name} added to measures list.')
            return f'{measure} of {self.name} added to measures list.'

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
            print(f'{measure} of {self.name} removed from measures list.')
        else:
            print(f'{measure} of {self.name} not found in measures list.')


class Recipe(RealThing):
    """docstring for Recipe."""

    def __init__(self, name, **kwargs):
        super().__init__(name)
        self.subpath = 'recipes'
        self.filename = name + '.json'
        self.ingredients = kwargs.get('ingredients', list())
        self.directions = kwargs.get('directions', '')
        self.is_healthy = kwargs.get('is_healthy', False)

    # Create operations for the Recipe class
    def add_ingredient(self, ingredient: Ingredient, quantity: str):
        self.ingredients.append({'name': ingredient.name, 'quantity': quantity})
        print(f'{ingredient.name} added to {self.name} ingredients list.')

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
    def remove_ingredient(self, ingredient):
        self.ingredients = [i for i in self.ingredients if i['name'] != ingredient.name]
        print(f"{ingredient.name} removed from {self.name} ingredients list.")

class Storage(RealThing):
    """docstring for Storage."""

    def __init__(self, name, **kwargs):
        super().__init__(name)
        self.subpath = 'storages'
        self.contents = kwargs.get('contents', dict())

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


class Kitchen(RealThing):
    def __init__(self, name, **kwargs):
        super().__init__(name)
        storages_path = kwargs.get('storages_path', './output/storages/')
        recipes_path = kwargs.get('recipes_path', './output/recipes/')
        ingredients_path = kwargs.get('ingredients_path', './output/ingredients/')

        self.storages = read_data(storages_path)
        self.recipes = read_data(recipes_path)
        self.ingredients = read_data(ingredients_path)

    def display_storages(self):
        for s in self.storages.values():
            print(s['name'])

    def display_recipes(self):
        for r in self.recipes.values():
            print(r['name'])

    def display_ingredients(self):
        for i in self.ingredients.values():
            print(i['name'])

    def show_inventory(self):
        for storage in self.storages.values():
            print(f"{storage['name']}/")
            for item_name, quantity in storage['contents'].items():
                print(f"  ├── {item_name} ({quantity})")
    def refresh_data(self, **kwargs):
        storages_path = kwargs.get('storages_path', './output/storages/')
        recipes_path = kwargs.get('recipes_path', './output/recipes/')
        ingredients_path = kwargs.get('ingredients_path', './output/ingredients/')

        self.storages = read_data(storages_path)
        self.recipes = read_data(recipes_path)
        self.ingredients = read_data(ingredients_path)