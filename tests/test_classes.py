import pytest
import os
import json

from meal_planner.classes import RealThing, Ingredient, Recipe, Storage, Kitchen
from meal_planner.generator import load_record


# RealThing tests
@pytest.fixture
def real_thing():
    return RealThing('TestThing')


def test_set_subpath(real_thing):
    subpath = 'test_subpath'
    assert real_thing.set_subpath(subpath) == subpath
    assert real_thing.subpath == subpath


def test_set_filename(real_thing):
    filename = 'test_filename'
    full_filename = filename + '.json'
    assert real_thing.set_filename(filename) == full_filename


def test_save_self_without_subpath(real_thing):
    with pytest.raises(ValueError, match='Subpath not set.'):
        real_thing.save_self()


def test_save_self_without_filename(real_thing):
    with pytest.raises(ValueError, match='Filename not set.'):
        real_thing.set_subpath('test_subpath')
        real_thing.save_self()


def test_save_self(tmp_path, real_thing):
    real_thing.set_subpath('test_subpath')
    real_thing.set_filename('test_filename')
    real_thing.output_path = str(tmp_path)

    save_message = real_thing.save_self()
    expected_path = os.path.join(tmp_path, 'test_subpath', 'test_filename.json')

    assert os.path.exists(expected_path)
    assert save_message == 'TestThing saved to test_subpath.'

    with open(expected_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert data['name'] == 'TestThing'
        assert data['subpath'] == 'test_subpath'
        assert data['filename'] == 'test_filename.json'


# Ingredient tests
@pytest.fixture
def ingredient():
    return Ingredient('Tomato')


def test_set_state(ingredient):
    response = ingredient.set_state('Fresh')
    assert ingredient.state == 'Fresh'
    assert response == 'State has been set to "Fresh".'

    response = ingredient.set_state('Fresh')
    assert response == 'State is already set to "Fresh".'


def test_add_measure(ingredient):
    measure = {'quantity': '2 cups'}
    ingredient.add_measure(measure)
    assert measure in ingredient.measures


def test_set_expiration(ingredient):
    response = ingredient.set_expiration('2023-12-31')
    assert ingredient.expiration == '2023-12-31'
    assert response == 'Expiration has been set to "2023-12-31".'

    response = ingredient.set_expiration('2023-12-31')
    assert response == 'Expiration is already set to "2023-12-31".'


def test_set_location(ingredient):
    response = ingredient.set_location('Fridge')
    assert ingredient.location == 'Fridge'
    assert response == 'Location has been set to "Fridge".'

    response = ingredient.set_location('Fridge')
    assert response == 'Location is already set to "Fridge".'


def test_get_measures(ingredient):
    measure = {'quantity': '2 cups'}
    ingredient.add_measure(measure)
    assert ingredient.get_measures() == [measure]


def test_get_state(ingredient):
    ingredient.set_state('Fresh')
    assert ingredient.get_state() == 'Fresh'


def test_get_expiration(ingredient):
    ingredient.set_expiration('2023-12-31')
    assert ingredient.get_expiration() == '2023-12-31'


def test_remove_measure(ingredient):
    measure = {'quantity': '2 cups'}
    ingredient.add_measure(measure)
    ingredient.remove_measure(measure)
    assert measure not in ingredient.measures

    response = ingredient.remove_measure(measure)
    assert response is None  # No output expected for non-existent measure


def test_save_ingredient(tmp_path, ingredient):
    ingredient.set_subpath('ingredients')
    ingredient.set_filename('test_ingredient')
    ingredient.output_path = str(tmp_path)
    ingredient.add_measure('2 cups')
    ingredient.set_state('Fresh')
    ingredient.set_expiration('2023-12-31')
    ingredient.set_location('Fridge')

    save_message = ingredient.save_self()

    expected_path = os.path.join(tmp_path, 'ingredients', 'test_ingredient.json')
    assert os.path.exists(expected_path)
    assert save_message == 'Tomato saved to ingredients.'

    with open(expected_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert data['name'] == 'Tomato'
        assert data['subpath'] == 'ingredients'
        assert data['filename'] == 'test_ingredient.json'
        assert data['measures'] == ['2 cups']
        assert data['state'] == 'Fresh'
        assert data['expiration'] == '2023-12-31'
        assert data['location'] == 'Fridge'


def test_str(ingredient):
    assert str(ingredient) == 'Tomato'


def test_ingredient_with_kwargs():
    ingredient = Ingredient('Tomato', state='Fresh', measures=[{'quantity': '1 cup'}], expiration='2023-12-31',
                            location='Fridge')
    assert ingredient.name == 'Tomato'
    assert ingredient.state == 'Fresh'
    assert ingredient.measures == [{'quantity': '1 cup'}]
    assert ingredient.expiration == '2023-12-31'
    assert ingredient.location == 'Fridge'


def test_ingredient_without_kwargs():
    ingredient = Ingredient('Tomato')
    assert ingredient.name == 'Tomato'
    assert ingredient.state == ''
    assert ingredient.measures == []
    assert ingredient.expiration == ''
    assert ingredient.location == ''


def test_add_measure_new(ingredient):
    measure = '2 cups'
    response = ingredient.add_measure(measure)
    assert measure in ingredient.measures
    assert response == '2 cups of Tomato added to measures list.'


def test_add_measure_duplicate(ingredient):
    measure = '2 cups'
    ingredient.add_measure(measure)
    response = ingredient.add_measure(measure)
    assert ingredient.measures.count(measure) == 1
    assert response == '2 cups of Tomato already in measures list.'


def test_set_macros():
    ingredient = Ingredient('Tomato')

    # Test setting macros for the first time
    response = ingredient.set_macros({'carbs': 'low', 'fats': 'medium', 'protein': 'high'})
    assert ingredient.macros == {'carbs': 'low', 'fats': 'medium', 'protein': 'high'}
    assert response == "Macros have been set to {'carbs': 'low', 'fats': 'medium', 'protein': 'high'}."

    # Test setting the same macros again
    response = ingredient.set_macros({'carbs': 'low', 'fats': 'medium', 'protein': 'high'})
    assert response == "Macros are already set to {'carbs': 'low', 'fats': 'medium', 'protein': 'high'}."

    # Test changing the macros
    response = ingredient.set_macros({'carbs': 'medium', 'fats': 'low', 'protein': 'medium'})
    assert ingredient.macros == {'carbs': 'medium', 'fats': 'low', 'protein': 'medium'}
    assert response == "Macros have been set to {'carbs': 'medium', 'fats': 'low', 'protein': 'medium'}."

    # Test setting macros to an empty dictionary
    response = ingredient.set_macros({})
    assert ingredient.macros == {}
    assert response == "Macros have been set to {}."


# Test for set_meal_role method
def test_set_meal_role(ingredient):
    response = ingredient.set_meal_role('carb')
    assert ingredient.meal_role == 'carb'
    assert response == 'Meal role has been set to "carb".'

    response = ingredient.set_meal_role('carb')
    assert response == 'Meal role is already set to "carb".'


# Test for make_meal_plan method

# Recipe tests
@pytest.fixture
def recipe():
    return Recipe('Test Recipe')


def test_add_ingredient(recipe):
    ingredient = Ingredient('Bacon')
    quantity = '1 lb.'
    result = recipe.add_ingredient(ingredient, quantity)
    assert {'name': 'Bacon', 'quantity': quantity} in recipe.ingredients
    assert result == 'Bacon added to Test Recipe ingredients list.'

def test_add_ingredient_with_different_quantity():
    recipe = Recipe('BLT Sandwich')
    ingredient = Ingredient('Bacon')
    recipe.add_ingredient(ingredient, '2 slices')
    result = recipe.add_ingredient(ingredient, '3 slices')
    assert {'name': 'Bacon', 'quantity': '2 slices'} in recipe.ingredients
    assert {'name': 'Bacon', 'quantity': '3 slices'} in recipe.ingredients
    assert result == 'Bacon added to BLT Sandwich ingredients list.'

def test_add_ingredient_with_empty_quantity():
    recipe = Recipe('BLT Sandwich')
    ingredient = Ingredient('Bacon')
    result = recipe.add_ingredient(ingredient, '')
    assert {'name': 'Bacon', 'quantity': ''} in recipe.ingredients
    assert result == 'Bacon added to BLT Sandwich ingredients list.'

def test_add_ingredient_with_special_characters_in_quantity():
    recipe = Recipe('BLT Sandwich')
    ingredient = Ingredient('Bacon')
    result = recipe.add_ingredient(ingredient, '2 slices @ 50% off')
    assert {'name': 'Bacon', 'quantity': '2 slices @ 50% off'} in recipe.ingredients
    assert result == 'Bacon added to BLT Sandwich ingredients list.'

def test_add_ingredient_with_numeric_quantity():
    recipe = Recipe('BLT Sandwich')
    ingredient = Ingredient('Bacon')
    result = recipe.add_ingredient(ingredient, '100')
    assert {'name': 'Bacon', 'quantity': '100'} in recipe.ingredients
    assert result == 'Bacon added to BLT Sandwich ingredients list.'

def test_add_ingredient_with_none_quantity():
    recipe = Recipe('BLT Sandwich')
    ingredient = Ingredient('Bacon')
    result = recipe.add_ingredient(ingredient, None)
    assert {'name': 'Bacon', 'quantity': None} in recipe.ingredients
    assert result == 'Bacon added to BLT Sandwich ingredients list.'

def test_add_directions(recipe):
    directions = 'Cook the bacon until crispy.'
    recipe.add_directions(directions)
    assert recipe.directions == directions

def test_add_empty_directions(recipe):
    directions = ''
    recipe.add_directions(directions)
    assert recipe.directions == directions

def test_add_long_directions(recipe):
    directions = ' '.join(['Step'] * 1000)
    recipe.add_directions(directions)
    assert recipe.directions == directions

def test_add_directions_with_special_characters(recipe):
    directions = 'Preheat oven to 350°F. Mix ingredients & bake for 20-25 minutes.'
    recipe.add_directions(directions)
    assert recipe.directions == directions

def test_add_directions_with_newlines(recipe):
    directions = 'Step 1: Preheat oven.\nStep 2: Mix ingredients.\nStep 3: Bake.'
    recipe.add_directions(directions)
    assert recipe.directions == directions

def test_add_directions_with_unicode(recipe):
    directions = 'Mix ingredients: 1 cup of flour, 2 eggs, and 1/2 cup of milk. 🍰'
    recipe.add_directions(directions)
    assert recipe.directions == directions

def test_set_health_value(recipe):
    response = recipe.set_health_value(True)
    assert recipe.is_healthy == True
    assert response == '"is_healthy" has been set to "True".'

    response = recipe.set_health_value(True)
    assert response == '"is_healthy" is already set to "True".'


def test_get_ingredients(recipe):
    ingredient = Ingredient('Bacon')
    quantity = '1 lb.'
    recipe.add_ingredient(ingredient, quantity)
    assert recipe.get_ingredients() == [{'name': 'Bacon', 'quantity': '1 lb.'}]


def test_get_directions(recipe):
    directions = 'Cook the bacon until crispy.'
    recipe.add_directions(directions)
    assert recipe.get_directions() == directions


def test_get_health_value(recipe):
    recipe.set_health_value(True)
    assert recipe.get_health_value() == True


def test_remove_ingredient(recipe):
    ingredient = Ingredient('Bacon')
    quantity = '1 lb.'
    recipe.add_ingredient(ingredient, quantity)

    # Ensure the ingredient is added
    assert {'name': 'Bacon', 'quantity': '1 lb.'} in recipe.ingredients

    # Remove the ingredient
    recipe.remove_ingredient(ingredient)

    # Ensure the ingredient is removed
    assert {'name': 'Bacon', 'quantity': '1 lb.'} not in recipe.ingredients

    # Try to remove the ingredient again and check for no output
    response = recipe.remove_ingredient(ingredient)
    assert response is None


def test_save_recipe(recipe):
    recipe.set_subpath('recipes')
    recipe.set_filename('test_recipe')
    recipe.output_path = 'output'
    ingredient = Ingredient('Bacon')
    recipe.add_ingredient(ingredient, '1 lb.')
    recipe.add_directions('Cook the bacon until crispy.')
    recipe.set_health_value(True)
    save_message = recipe.save_self()

    expected_path = os.path.join('output', 'recipes', 'test_recipe.json')
    assert os.path.exists(expected_path)
    assert save_message == 'Test Recipe saved to recipes.'

    with open(expected_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert data['name'] == 'Test Recipe'
        assert data['subpath'] == 'recipes'
        assert data['filename'] == 'test_recipe.json'
        assert data['ingredients'] == [{'name': 'Bacon', 'quantity': '1 lb.'}]
        assert data['directions'] == 'Cook the bacon until crispy.'
        assert data['is_healthy'] == True


# Storage tests
@pytest.fixture
def storage():
    return Storage('Pantry')


@pytest.fixture
def item():
    return Ingredient('Canned Beans')


def test_add_item(storage, item):
    storage.add_item(item)
    assert storage.contents[item.name] == 1

    storage.add_item(item)
    assert storage.contents[item.name] == 2


def test_get_contents(storage, item):
    storage.add_item(item)
    contents = storage.get_contents()
    assert contents[item.name] == 1


def test_remove_item(storage, item):
    storage.add_item(item)
    storage.remove_item(item)
    assert storage.contents[item.name] == 0

    storage.remove_item(item)
    assert storage.contents[item.name] == 0  # No negative values


def test_save_storage(tmp_path, storage):
    storage.set_subpath('storages')
    storage.set_filename('test_storage')
    storage.output_path = str(tmp_path)
    item = Ingredient('Canned Beans')
    storage.add_item(item)

    save_message = storage.save_self()

    expected_path = os.path.join(tmp_path, 'storages', 'test_storage.json')
    assert os.path.exists(expected_path)
    assert save_message == 'Pantry saved to storages.'

    with open(expected_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert data['name'] == 'Pantry'
        assert data['subpath'] == 'storages'
        assert data['filename'] == 'test_storage.json'
        assert data['contents'] == {'Canned Beans': 1}


@pytest.fixture
def kitchen(tmp_path):
    storages_path = tmp_path / "storages"
    recipes_path = tmp_path / "recipes"
    ingredients_path = tmp_path / "ingredients"
    storages_path.mkdir()
    recipes_path.mkdir()
    ingredients_path.mkdir()

    # Create sample data
    with open(storages_path / "pantry.json", "w") as f:
        json.dump({"name": "Pantry", "contents": {"Canned Beans": 1}}, f)
    with open(recipes_path / "blt_sandwich.json", "w") as f:
        json.dump({"name": "BLT Sandwich", "ingredients": [{"name": "Bacon", "quantity": "1 lb."}],
                   "directions": "Cook the bacon until crispy.", "is_healthy": False,
                   "meal_roles": [
                       "protein",
                       "carb",
                       "veggie"
                   ], "subpath": "recipes"}, f)
    with open(ingredients_path / "tomato.json", "w") as f:
        json.dump({"name": "Tomato", "state": "Fresh", "measures": ["1 cup"], "expiration": "2023-12-31",
                   "location": "Fridge", "macros": {"protein": "low", "fats": "low", "carbs": "low"},
                   "meal_role": "veggie"}, f)
    with open(ingredients_path / "bacon.json", "w") as f:
        json.dump({"name": "bacon", "state": "solid", "measures": ["lb"], "expiration": "2023-12-31",
                   "location": "fridge", "macros": {"protein": "high", "fats": "high", "carbs": "low"},
                   "meal_role": "protein"}, f)
    with open(ingredients_path / "bread.json", "w") as f:
        json.dump({"name": "bread", "state": "solid", "measures": ["slice"], "expiration": "2023-12-31",
                   "location": "cupboard", "macros": {"protein": "low", "fats": "low", "carbs": "high"},
                   "meal_role": "carb"}, f)

    return Kitchen("Test Kitchen", storages_path=storages_path, recipes_path=recipes_path,
                   ingredients_path=ingredients_path)


def test_display_storages(kitchen, capsys):
    kitchen.display_storages()
    captured = capsys.readouterr()
    assert "Pantry" in captured.out


def test_display_recipes(kitchen, capsys):
    kitchen.display_recipes()
    captured = capsys.readouterr()
    assert "BLT Sandwich" in captured.out


def test_display_ingredients(kitchen, capsys):
    kitchen.display_ingredients()
    captured = capsys.readouterr()
    assert "Tomato" in captured.out


def test_show_inventory(kitchen, capsys):
    kitchen.show_inventory()
    captured = capsys.readouterr()
    assert "Pantry/" in captured.out
    assert "Canned Beans (1)" in captured.out


def test_refresh_data(kitchen, tmp_path):
    new_storages_path = tmp_path / "new_storages"
    new_recipes_path = tmp_path / "new_recipes"
    new_ingredients_path = tmp_path / "new_ingredients"
    new_storages_path.mkdir()
    new_recipes_path.mkdir()
    new_ingredients_path.mkdir()

    with open(new_storages_path / "fridge.json", "w") as f:
        json.dump({"name": "Fridge", "contents": {"Milk": 2}}, f)
    with open(new_recipes_path / "tomato_soup.json", "w") as f:
        json.dump({"name": "Tomato Soup", "ingredients": [{"name": "Tomato", "quantity": "2 cups"}],
                   "directions": "Blend the tomatoes.", "is_healthy": True,
                   "meal_roles": [
                       "veggie"
                   ], "subpath": "recipes"}, f)
    with open(new_ingredients_path / "lettuce.json", "w") as f:
        json.dump({"name": "Lettuce", "state": "Fresh", "measures": ["1 leaf"], "expiration": "2023-12-31",
                   "location": "Fridge", "macros": {"protein": "low", "fats": "low", "carbs": "low"},
                   "meal_role": "veggie"}, f)

    kitchen.refresh_data(storages_path=new_storages_path, recipes_path=new_recipes_path,
                         ingredients_path=new_ingredients_path)

    assert 'fridge' in [s for s in kitchen.storages]
    assert 'tomato_soup' in [r for r in kitchen.recipes]
    assert ('lettuce') in [i for i in kitchen.ingredients]


def test_make_meal_plan_zero_days(kitchen):
    meal_plan = kitchen.make_meal_plan(0)
    assert meal_plan == {}


def test_make_meal_plan_single_day(kitchen):
    meal_plan = kitchen.make_meal_plan(1)
    assert len(meal_plan) == 1
    assert 'veggie' in meal_plan[0]
    assert 'protein' in meal_plan[0]
    assert 'carb' in meal_plan[0]


def test_make_meal_plan_multiple_days(kitchen):
    meal_plan = kitchen.make_meal_plan(3)
    assert len(meal_plan) == 3
    for day in range(3):
        assert 'veggie' in meal_plan[day]
        assert 'protein' in meal_plan[day]
        assert 'carb' in meal_plan[day]


def test_make_meal_plan_no_ingredients(kitchen):
    kitchen.ingredients = {}
    kitchen.storages['pantry']['contents'] = {}
    meal_plan = kitchen.make_meal_plan(1)
    assert len(meal_plan) == 1
    assert meal_plan[0].get('veggie', []) == []
    assert meal_plan[0].get('protein', []) == []
    assert meal_plan[0].get('carb', []) == []


def test_make_meal_plan_no_meal_roles(kitchen):
    for ingredient in kitchen.ingredients.values():
        ingredient['meal_role'] = ''
    meal_plan = kitchen.make_meal_plan(1)
    assert len(meal_plan) == 1
    assert meal_plan[0]['veggie'] == []
    assert meal_plan[0]['protein'] == []
    assert meal_plan[0]['carb'] == []


def test_make_meal_plan_with_meal_roles_and_storage(kitchen):
    kitchen.ingredients['tomato']['meal_role'] = 'veggie'
    kitchen.ingredients['tomato']['location'] = 'pantry'
    kitchen.ingredients['bacon']['meal_role'] = 'protein'
    kitchen.ingredients['bacon']['location'] = 'pantry'
    kitchen.ingredients['bread']['meal_role'] = 'carb'
    kitchen.ingredients['bread']['location'] = 'pantry'
    kitchen.storages['pantry']['contents'] = {'tomato': 1, 'bacon': 1, 'bread': 1}
    meal_plan = kitchen.make_meal_plan(1)
    assert len(meal_plan) == 1
    assert meal_plan[0]['veggie']['name'].lower() == 'tomato'
    assert meal_plan[0]['protein']['name'].lower() == 'bacon'
    assert meal_plan[0]['carb']['name'].lower() == 'bread'


def test_make_meal_plan_excludes_non_storage_items(kitchen):
    kitchen.ingredients['tomato']['meal_role'] = 'veggie'
    kitchen.ingredients['tomato']['location'] = 'pantry'
    kitchen.ingredients['bacon']['meal_role'] = 'protein'
    kitchen.ingredients['bacon']['location'] = 'pantry'
    kitchen.ingredients['bread']['meal_role'] = 'carb'
    kitchen.ingredients['bread']['location'] = ''  # 'bread' is not in storage
    kitchen.storages['pantry']['contents'] = {'tomato': 1, 'bacon': 1}  # 'bread' is not in storage
    meal_plan = kitchen.make_meal_plan(1)
    assert len(meal_plan) == 1
    assert meal_plan[0]['veggie']['name'].lower() == 'tomato'
    assert meal_plan[0]['protein']['name'].lower() == 'bacon'
    assert all(ingredient['location'] != '' for role in meal_plan[0].values() for ingredient in role if isinstance(ingredient, dict))  # No ingredient should have an empty location


def test_add_meal_role(kitchen):
    recipe = load_record(kitchen.recipes['blt_sandwich'])
    result = recipe.add_meal_role('breakfast')
    assert 'breakfast' in recipe.meal_roles
    assert result == 'breakfast added to meal roles list.'

    result = recipe.add_meal_role('breakfast')
    assert result == 'breakfast already in meal roles list.'


def test_remove_meal_role(kitchen):
    recipe = load_record(kitchen.recipes['blt_sandwich'])
    recipe.add_meal_role('breakfast')
    result = recipe.remove_meal_role('breakfast')
    assert 'breakfast' not in recipe.meal_roles
    assert result == 'breakfast removed from meal roles list.'

    result = recipe.remove_meal_role('breakfast')
    assert result == 'breakfast not found in meal roles list.'
