import pytest
import os
import json

from meal_planner.classes import RealThing, Ingredient, Recipe, Storage, MealPlan

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
    assert real_thing.set_filename(filename) == filename
    assert real_thing.filename == filename

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

def test_str(ingredient):
    assert str(ingredient) == 'Tomato'

# Recipe tests
@pytest.fixture
def recipe():
    return Recipe('Test Recipe')

def test_add_ingredients(recipe):
    ingredients = [{'name': 'Bacon', 'quantity': '1 lb.'}]
    recipe.add_ingredients(ingredients)
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0]['name'] == 'Bacon'

def test_add_directions(recipe):
    directions = 'Cook the bacon until crispy.'
    recipe.add_directions(directions)
    assert recipe.directions == directions

def test_set_health_value(recipe):
    response = recipe.set_health_value(True)
    assert recipe.is_healthy == True
    assert response == '"is_healthy" has been set to "True".'

    response = recipe.set_health_value(True)
    assert response == '"is_healthy" is already set to "True".'

def test_get_ingredients(recipe):
    ingredients = [{'name': 'Bacon', 'quantity': '1 lb.'}]
    recipe.add_ingredients(ingredients)
    assert recipe.get_ingredients() == ingredients

def test_get_directions(recipe):
    directions = 'Cook the bacon until crispy.'
    recipe.add_directions(directions)
    assert recipe.get_directions() == directions

def test_get_health_value(recipe):
    recipe.set_health_value(True)
    assert recipe.get_health_value() == True

def test_remove_ingredient(recipe):
    ingredient = {'name': 'Bacon', 'quantity': '1 lb.'}
    recipe.add_ingredients([ingredient])
    recipe.remove_ingredient(ingredient)
    assert ingredient not in recipe.ingredients

    response = recipe.remove_ingredient(ingredient)
    assert response is None  # No output expected for non-existent ingredient

# Storage tests
@pytest.fixture
def storage():
    return Storage('Pantry')

@pytest.fixture
def item():
    return RealThing('Canned Beans')

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

# MealPlan tests

@pytest.fixture
def meal_plan():
    recipes = {
        'Healthy Recipe 1': {'is_healthy': True},
        'Healthy Recipe 2': {'is_healthy': True},
        'Fatty Recipe 1': {'is_healthy': False},
        'Fatty Recipe 2': {'is_healthy': False}
    }
    return MealPlan(recipes, 7)

def test_split_recipes(meal_plan):
    meal_plan.split_recipes()
    assert len(meal_plan.healthy_recipes) == 2
    assert len(meal_plan.fatty_recipes) == 2

def test_make_plan(meal_plan):
    meal_plan.split_recipes()
    plan = meal_plan.make_plan()
    assert len(plan) == 7
    assert plan.count('Healthy Recipe 1') + plan.count('Healthy Recipe 2') == 5
    assert plan.count('Fatty Recipe 1') + plan.count('Fatty Recipe 2') == 2
