"""
This module launches the command line app for generating, manipulating & visualizing a rubiks cube built on the architecture defined in this project.

"""
from typing import Union
from rubiks_cube.errors import InvalidOperationError
from rubiks_cube import (
    cube, 
    menu_options, 
    rotate_options, 
    invert_options, 
    shift_options, 
    shuffle_options,
    menu_options_funcs,
    rotate_options_params,
    invert_options_params,
    shift_options_params
)

def main():
    print('#################################################################################')
    print('Command Line App Starting Up')
    print('########################################')
    print('BUILDING RUBIKS CUBE...\n')
    
    while True:
        
        print(f'{cube}\n')
        
        main_response = run_menu('Main Menu', menu_options, True)
        if main_response is None:
            continue
        if main_response == 'q':
            exit()

        if main_response == 0:
            while True:
                rotate_response = run_menu('Rotations', rotate_options, False)
                if rotate_response is None:
                    continue
                if rotate_response == 'b':
                    break
                if rotate_response == 'q':
                    exit()
                try:
                    menu_options_funcs[main_response](rotate_options_params[rotate_response])
                    break
                except IndexError:
                    print('\nInvalid input. Please input a valid choice.\n')
                    continue
        elif main_response == 1:
            while True:
                invert_response = run_menu('Inversions', invert_options, False)
                if invert_response is None:
                    continue
                if invert_response == 'b':
                    break
                if invert_response == 'q':
                    exit()
                try:
                    menu_options_funcs[main_response](invert_options_params[invert_response])
                    break
                except IndexError:
                    print('\nInvalid input. Please input a valid choice.\n')
                    continue
        elif main_response == 2:
            while True:
                shift_response = run_menu('Shifts', shift_options, False)
                if shift_response is None:
                    continue
                if shift_response == 'b':
                    break
                if shift_response == 'q':
                    exit()
                try:
                    menu_options_funcs[main_response](shift_options_params[shift_response])
                    break
                except IndexError:
                    print('\nInvalid input. Please input a valid choice.\n')
                    continue
        elif main_response == 3:
            menu_options_funcs[main_response]()
        elif main_response == 4:
            while True:
                shuffle_response = run_menu('Shuffle Cube', shuffle_options, False)
                if shuffle_response is None:
                    continue
                if shuffle_response == 'b':
                    break
                if shuffle_response == 'q':
                    exit() 
                if shuffle_response == 0:
                    # random
                    menu_options_funcs[main_response]()
                    break
                elif shuffle_response == 1:
                    while True:
                        inp = input("\nEnter number of operations [int, 'b' for back or 'q' for quit]: ")
                        try:
                            num_ops = int(inp)
                        except ValueError:
                            if inp == 'b':
                                break
                            if inp == 'q':
                                exit()
                            print('\nInvalid input. Please input a valid choice.\n')
                            continue
                        menu_options_funcs[main_response](num_ops)
                        break
                else:
                    print('\nInvalid input. Please input a valid choice.\n')
                    continue
        elif main_response == 5:
            try:
                menu_options_funcs[main_response]()
            except InvalidOperationError:
                print('\nCannot unshuffle a solved cube. Perform some operations before trying to unshuffle.\n')
        else:
            print('\nInvalid input. Please input a valid choice.\n')
            continue


def run_menu(title: str, options: list[str], is_main=False) -> Union[int, str, None]:
    """
    This function displays and reads in user input to perform various operations on a rubiks cube instance.

    Args:
        title (str): Menu title to be displayed
        options (list): List of menu options
        is_main (bool, optional): Flag indicating if the menu to be displayed is the main menu. Defaults to False.

    Returns:
        int | str | None: returns user's operation choice (int or str) or None (if invalid input)

    """
    print(f'\n{title}:\n')
    for idx, option in enumerate(options):
        print(f'{idx+1}. {option}')
    if is_main:
        response = input(f"\nEnter response [1-{idx+1} or 'q' for quit]: ")
    else:
        response = input(f"\nEnter response [1-{idx+1}, 'b' for back or 'q' for quit]: ")
    try:
        idx_chosen = int(response) - 1
    except:
        if response == 'q':
            return response
        if not is_main and response == 'b':
            return response
        else:
            print('\nInvalid input. Please input a valid choice.\n')
            return None
        
    return idx_chosen


if __name__ == "__main__":
    main()
