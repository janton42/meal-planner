import os
import csv
import json
import random
import logging

from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# write date out as json input should be a python dictionary
def write_data(data: dict, path: str):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f'Error writing data to {path}: {e}')
        raise


# read json file to a python dictionary
def read_data(path: str) -> dict:
    path = Path(path)
    objects = os.listdir(path)
    data = dict()
    for obj in objects:
        with open(path / obj, 'r') as f:
            name = obj.split('.')[0]
            record = json.load(f)
            data.update(
                {name: record}
            )
    return data


def shuffle(deck: list) -> list:
    max_i = len(deck)
    for i in range(max_i):
        j = random.randint(0, max_i - 1)
        deck[i], deck[j] = deck[j], deck[i]

    return deck


def plan_display(plan):
    for day in plan:
        message = f"Day {day}:\n |--veggie: {plan[day]['veggie']['name']}\n |--protein: {plan[day]['protein']['name']}\n |--carb: {plan[day]['carb']['name']}\n"
        print(message)
    print()  # Add a newline after each day
