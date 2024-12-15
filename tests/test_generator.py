import pytest
from meal_planner.classes import Ingredient, Recipe, Storage
from meal_planner.generator import load_record

def test_load_record_ingredient():
    record = {
        'subpath': 'ingredients',
        'name': 'Tomato',
        'state': 'Fresh',
        'measures': ['1 cup'],
        'expiration': '2023-12-31',
        'location': 'Fridge'
    }
    item = load_record(record)
    assert isinstance(item, Ingredient)
    assert item.name == 'Tomato'
    assert item.state == 'Fresh'
    assert item.measures == ['1 cup']
    assert item.expiration == '2023-12-31'
    assert item.location == 'Fridge'

def test_load_record_recipe():
    record = {
        'subpath': 'recipes',
        'name': 'BLT Sandwich',
        'ingredients': [{'name': 'Bacon', 'quantity': '1 lb.'}],
        'directions': 'Cook the bacon until crispy.',
        'is_healthy': False
    }
    item = load_record(record)
    assert isinstance(item, Recipe)
    assert item.name == 'BLT Sandwich'
    assert item.ingredients == [{'name': 'Bacon', 'quantity': '1 lb.'}]
    assert item.directions == 'Cook the bacon until crispy.'
    assert item.is_healthy == False

def test_load_record_storage():
    record = {
        'subpath': 'storages',
        'name': 'Pantry',
        'contents': {'Canned Beans': 1}
    }
    item = load_record(record)
    assert isinstance(item, Storage)
    assert item.name == 'Pantry'
    assert item.contents == {'Canned Beans': 1}

def test_load_record_invalid_subpath(capsys):
    record = {
        'subpath': 'unknown',
        'name': 'Unknown'
    }
    item = load_record(record)
    captured = capsys.readouterr()
    assert item == ''
    assert 'Record not found.' in captured.out
