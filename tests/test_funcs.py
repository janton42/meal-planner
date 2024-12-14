import json

from meal_planner.funcs import write_data, read_data, shuffle


def test_write_data(tmp_path):
    data = {"key": "value"}
    file_path = tmp_path / "test.json"
    write_data(data, str(file_path))

    assert file_path.exists()
    with open(file_path, 'r', encoding='utf-8') as f:
        loaded_data = json.load(f)
    assert loaded_data == data


def test_read_data(tmp_path):
    data = {"key": "value"}
    file_path = tmp_path / "test.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)

    read_data_result = read_data(str(tmp_path) + '/')
    assert read_data_result == {"test.json": data}


def test_shuffle():
    deck = [1, 2, 3, 4, 5]
    shuffled_deck = shuffle(deck.copy())

    assert len(shuffled_deck) == len(deck)
    assert set(shuffled_deck) == set(deck)
    assert shuffled_deck != deck  # There's a small chance this could fail if shuffle returns the same order