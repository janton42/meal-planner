import json
import os

from meal_planner.funcs import write_data, read_data, shuffle, plan_display, pointer_return


def test_write_data(tmp_path):
    data = {"key": "value"}
    file_path = tmp_path / "test.json"
    write_data(data, str(file_path))

    assert file_path.exists()
    with open(file_path, 'r', encoding='utf-8') as f:
        loaded_data = json.load(f)
    assert loaded_data == data


def test_write_data_error_handling(tmp_path):
    data = {"key": "value"}
    invalid_path = tmp_path / "non_existent_dir/test.json"

    # Remove write permissions to trigger an OSError
    os.chmod(tmp_path, 0o400)

    try:
        write_data(data, str(invalid_path))
    except Exception as e:
        assert isinstance(e, OSError)
    finally:
        # Restore write permissions
        os.chmod(tmp_path, 0o700)


def test_read_data(tmp_path):
    data = {"key": "value"}
    file_path = tmp_path / "test.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)

    read_data_result = read_data(str(tmp_path) + '/')
    assert read_data_result == {"test": data}


def test_shuffle():
    deck = [1, 2, 3, 4, 5]
    shuffled_deck = shuffle(deck.copy())

    assert len(shuffled_deck) == len(deck)
    assert set(shuffled_deck) == set(deck)
    assert shuffled_deck != deck  # There's a small chance this could fail if shuffle returns the same order


def test_plan_display(capsys):
    plan = {
        0: {
            'veggie': {'name': 'Carrot'},
            'protein': {'name': 'Chicken'},
            'carb': {'name': 'Rice'}
        },
        1: {
            'veggie': {'name': 'Broccoli'},
            'protein': {'name': 'Beef'},
            'carb': {'name': 'Potato'}
        }
    }

    plan_display(plan)
    captured = capsys.readouterr()
    expected_output = (
        "Day 0:\n"
        " |--veggie: Carrot\n"
        " |--protein: Chicken\n"
        " |--carb: Rice\n\n"
        "Day 1:\n"
        " |--veggie: Broccoli\n"
        " |--protein: Beef\n"
        " |--carb: Potato\n\n\n"
    )
    assert captured.out == expected_output

def test_pointer_return():
    assert pointer_return(10, 5) == 5
    assert pointer_return(10, 10) == 10
    assert pointer_return(10, 11) == 0
    assert pointer_return(0, 1) == 0