import os
import csv
import json
import random

# write date out as json input should be a python dictionary
def write_data(data: dict, path: str):
    # Print the path to debug
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# read json file to a python dictionary
def read_data(path: str)-> dict:
    objects = os.listdir(path)
    data = dict()
    for obj in objects:
        with open(path + obj, 'r') as f:
            record = json.load(f)
            data.update(
                {obj: record}
                )
    return data

def shuffle(deck: list)->list:
    max_i = len(deck)
    for i in range(max_i):
        j = random.randint(0, max_i - 1)
        deck[i], deck[j] = deck[j], deck[i]

    return deck
