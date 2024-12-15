import pytest
from unittest.mock import patch
from meal_planner.classes import Kitchen, Ingredient, Recipe, Storage
from meal_planner.main import main


@pytest.fixture
def kitchen():
    return Kitchen('test_kitchen')


def test_make_meal_plan(kitchen):
    with patch('meal_planner.main.plan_display') as mock_display:
        with patch('builtins.input', side_effect=['1', '2', '0']):
            main(kitchen)
            mock_display.assert_called_once()


def test_show_inventory(kitchen):
    with patch('builtins.input', side_effect=['2', '0']):
        with patch.object(kitchen, 'show_inventory') as mock_show_inventory:
            main(kitchen)
            mock_show_inventory.assert_called_once()


def test_add_ingredient(kitchen):
    with patch('builtins.input', side_effect=['3', 'Tomato', 'veggie', 'Fridge', '0']):
        with patch.object(Ingredient, 'save_self') as mock_save:
            main(kitchen)
            mock_save.assert_called_once()

def test_add_recipe(kitchen):
    with patch('builtins.input', side_effect=['4', 'Spaghetti', '1', 'Boil pasta', '2', 'Pasta', '1 lb',
                                              'n', '3', '0']):
        with patch.object(Recipe, 'save_self') as mock_save:
            main(kitchen)
            mock_save.assert_called_once()


def test_add_storage_location(kitchen):
    with patch('builtins.input', side_effect=['5', 'Pantry', '0']):
        with patch.object(Storage, 'save_self') as mock_save:
            main(kitchen)
            mock_save.assert_called_once()


