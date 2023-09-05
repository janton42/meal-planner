import os
import csv

from meal_planner.main import main
from meal_planner.classes import Recipe


test_recipe_name = 'Test Recipe'
test_recipe = Recipe(test_recipe_name)

def test_main():
    output = main()
    assert test_recipe.name + '.json' in output

def test_recipes():
    assert test_recipe.name == test_recipe_name

def test_add_ingredients():
    test_recipe.add_ingredients([{'name': 'Bacon', 'quantity': '1 lb.'}])
    assert len(test_recipe.ingredients) == 1
    assert test_recipe.ingredients[0]['name'] == 'Bacon'

def test_list_ingredients():
    shopping_list = test_recipe.list_ingredients()
    assert shopping_list[0]['name'] == 'Bacon'
    assert shopping_list[0]['quantity'] == '1 lb.'

def test_set_health_value():
    response = test_recipe.set_health_value(False)

    assert test_recipe.is_healthy == False
    assert response == '"is_healthy" is already set to "False".'

    response = test_recipe.set_health_value(True)

    assert test_recipe.is_healthy == True
    assert response == '"is_healthy" has been set to "True".'

def test_save_self():
    save_message = test_recipe.save_self()
    assert save_message == f'{test_recipe.name} saved to Recipes.'

def test_export_ingredients():
    export_message = test_recipe.export_ingredients()
    assert export_message == f'Ingredient list for {test_recipe.name} exported'

# def test_plan_meals():
#     # plan_meals should:
#     meal_plan = main.plan_meals(
#         meal='dinner',
#         days=5,
#         health_percentage=25,
#         unhealthy_duration=2,
#     )
#
#     assert
        # read in db of recipes
        # take in a number of days as an integer
        # take in the percentage of healthy meals as an integer
        # take in a duration between unhealth meals in days as an integer
        #    (default is 3)
        # Shuffle recipe list
        # return a list of recipes following input constraints
            # If there are more days than there are recipes, repeat
            # recipes from shuffled list until days are full
