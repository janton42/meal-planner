import os
import csv

from funcs import read_data, write_data
from classes import Recipe, MealPlan


def main():
    # retreive data
    initial_data = read_data('meal_planner/output/recipes/')
    choice = int(input('\n\nWhat would you like to do?\n'
                        '(1) See Recipes\n'
                        '(2) Make meal plan\n'
                        '(9) Quit\n'
                        '*********'
                        '\n\n\n\nPlease enter your choice:  '
                        ))
    if choice == 1:
        print('\n' * 41)
        for r in initial_data:
            output = r.split('.')[0] + ' ' + str(initial_data[r]['is_healthy'])
            print(output)
        next = int(input('\n\nWhat next?\n'
                    '(1) Go back to main menu\n'
                    '(2) Add Recipe\n'
                    '(9) Quit\n'
                    '*********'
                    '\n\n\n\nPlease enter your choice:  '
                ))
        if next == 1:
            print('\n' * 50)
            main()
        if next == 2:
            name = input('Recipe Name:  ')
            new_recipe = Recipe(name)
            healthy = input('Is this recipe healthy (yes/no)?     ')
            if healthy == 'yes':
                new_recipe.set_health_value(True)
            else:
                new_recipe.set_health_value(False)
            new_recipe.save_self()
            main()
        elif next == 9:
            print('Good bye!')
        else:
            print('\n' * 41)
            print('***Invalid Input***\n\nReturning to main menu')
            main()
    elif choice == 2:
        days = input('How many days?      ')
        new_plan = MealPlan(initial_data, days)
        new_plan.make_plan()
        main()
    elif choice == 9:
        print('Good bye!')
    else:
        print('\n' * 41)
        print('***Invalid Input***\n\nReturning to main menu')
        main()

if __name__ == '__main__':
    print('\n' * 50)
    main()
