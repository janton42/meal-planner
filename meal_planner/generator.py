from meal_planner.classes import Ingredient, Recipe, Storage


def load_record(record: dict):
    item = ''
    if record['subpath'] == 'ingredients':
        item = Ingredient(**record)
    elif record['subpath'] == 'recipes':
        item = Recipe(**record)
    elif record['subpath'] == 'storages':
        item = Storage(**record)
    else:
        print('Record not found.')

    return item


def objectify(records: list[dict]) -> list:
    objects = list()
    for record in records:
        objects.append(load_record(record))
    return objects
