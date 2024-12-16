import os

from meal_planner.funcs import read_data, write_data, shuffle, pointer_return


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
        self.macros = kwargs.get('macros', dict())
        self.meal_role = kwargs.get('meal_role', '')

    # Create operations for the Ingredient class

    def set_meal_role(self, meal_role: str):
        if meal_role == self.meal_role:
            print(f'Meal role is already set to "{self.meal_role}".')
            return f'Meal role is already set to "{self.meal_role}".'
        else:
            self.meal_role = meal_role
            print(f'Meal role has been set to "{self.meal_role}".')
            return f'Meal role has been set to "{self.meal_role}".'

    def set_macros(self, macros: dict):
        if macros == self.macros:
            print(f'Macros are already set to {self.macros}.')
            return f'Macros are already set to {self.macros}.'
        else:
            self.macros = macros
            print(f'Macros have been set to {self.macros}.')
            return f'Macros have been set to {self.macros}.'

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
        self.meal_roles = kwargs.get('meal_roles', list())

    # Create operations for the Recipe class
    def add_meal_role(self, meal_role: str):
        if meal_role in self.meal_roles:
            print(f'{meal_role} already in meal roles list.')
            return f'{meal_role} already in meal roles list.'
        else:
            self.meal_roles.append(meal_role)
            print(f'{meal_role} added to meal roles list.')
            return f'{meal_role} added to meal roles list.'

    def add_ingredient(self, ingredient: Ingredient, quantity: str):
        new_ingredient = {'name': ingredient.name, 'quantity': quantity}
        if new_ingredient not in self.ingredients:
            self.ingredients.append(new_ingredient)
        success_message = f'{ingredient.name} added to {self.name} ingredients list.'
        print(success_message)
        return success_message

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

    def remove_meal_role(self, meal_role: str):
        if meal_role in self.meal_roles:
            self.meal_roles.remove(meal_role)
            print(f'{meal_role} removed from meal roles list.')
            return f'{meal_role} removed from meal roles list.'
        else:
            print(f'{meal_role} not found in meal roles list.')
            return f'{meal_role} not found in meal roles list.'


class Storage(RealThing):
    """docstring for Storage."""

    def __init__(self, name, **kwargs):
        super().__init__(name)
        self.subpath = 'storages'
        self.contents = kwargs.get('contents', dict())

    # Create operations for the Storage class
    def add_item(self, item: Ingredient):
        if item.name not in self.contents:
            self.contents[item.name] = 1
        else:
            self.contents[item.name] += 1
        item.location = self.name
        print(f'There are {self.contents[item.name]} {item.name} in {self.name}.')

    # Read operations for the Storage class
    def get_contents(self):
        return self.contents

    # Delete operations for the Storage class
    def remove_item(self, item: Ingredient):
        if self.contents[item.name] > 0:
            item.location = ''
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

    def make_meal_plan(self, days: int):
        """ Docstring for make_meal_plan
        Make a dictionary that will be the final meal plan.
        """

        meal_plan = dict()

        # Compile all the recipies, separated by meal roles
        #   Recipes can have multiple meal roles, stored as a list of strings,
        #   and may appear in multiple meal role lists
        veggie_recipies = shuffle([r for r in self.recipes.values()
                                   if 'veggie' in r['meal_roles']])
        protein_recipies = shuffle([r for r in self.recipes.values()
                                   if 'protein' in r['meal_roles']])
        carb_recipies = shuffle([r for r in self.recipes.values()
                                   if 'carb' in r['meal_roles']])

        # Compile ingredients in a similar fashion, grouped by meal role.
        #   Ingredients have only one meal role.
        #   Only ingredients in a storage location are included.
        veggie_ingredients = shuffle(
            [i for i in self.ingredients.values()
             if i['meal_role'] == 'veggie' and i['location'] != ''])
        protein_ingredients = shuffle(
            [i for i in self.ingredients.values()
             if i['meal_role'] == 'protein' and i['location'] != ''])
        carb_ingredients = shuffle(
            [i for i in self.ingredients.values()
             if i['meal_role'] == 'carb' and i['location'] != ''])

        # Combine the meal type lists so that the recipes are in the front, and will therefore be given priority in
        # planning
        veggies = veggie_recipies + veggie_ingredients
        proteins = protein_recipies + protein_ingredients
        carbs = carb_recipies + carb_ingredients

        # Set pointers for each meal type.
        v_pointer = 0
        p_pointer = 0
        c_pointer = 0
        for day in range(days):
            # Check each pointer against the length of its respective list's length. If the pointer is outside the
            # list range, pointer_return resets the pointer to 0
            v_pointer = pointer_return(limit=len(veggies)-1, pointer=v_pointer)
            p_pointer = pointer_return(limit=len(veggies) - 1, pointer=p_pointer)
            c_pointer = pointer_return(limit=len(carbs)-1, pointer=c_pointer)

            # Set each portion of the meal according to each role list and role pointer
            veggie = veggies[v_pointer]
            protein = proteins[p_pointer]
            carb = carbs[c_pointer]

            # Giving 'veggies' the priority, check to see if a selected recipe occupies multiple meal roles.
            # Set all appropriate meal roles, with 'proteins' and 'carbs' coming next in priority in that order.
            if veggie in proteins and veggie in carbs:
                protein, carb = veggie, veggie
            elif veggie in proteins:
                protein = veggie
            elif veggie in carbs:
                carb = veggie
            elif protein in veggies and protein in carbs:
                veggie, carb = protein, protein
            elif protein in veggies:
                veggie = protein
            elif protein in carbs:
                carb = protein
            elif carb in veggies and carb in proteins:
                protein, veggie = carb, carb
            elif carb in veggies:
                veggie = carb
            elif carb in proteins:
                protein = carb

            # Add the day's meal plan to the overall meal plan
            meal_plan[day] = {
                'veggie': veggie,
                'protein': protein,
                'carb': carb,
            }

            # Increment all role pointers by one.
            v_pointer += 1
            p_pointer += 1
            c_pointer += 1
        return meal_plan
