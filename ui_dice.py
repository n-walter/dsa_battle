import PySimpleGUI as sg
from typing import List, Dict, Any, Self

import random                   # roll dice automatically
import strings                  # translations

    
def get_dice_roll_line(id: str, die: int):
    info_text = f"1{strings.get_string("dice_char")}{die}: "
    default_value = str(random.randint(1, die))
    die_row = [sg.Text(info_text, size=(15, 1)), sg.VSeparator(pad=((10,0),(0,0))), sg.InputText(key=id, size=(5,1), default_text=default_value)]
    return die_row

def get_dice_rolls(dice: List[int], description: str = "") -> List[int]:
    """
    returns list of dice roll values for the list of provided dice.
   
    :param List[int] dice: List of dice to roll. int defines the "size" of the die
    :param str description: description of the dice to roll e.g. "Attack check for Gil against Steintroll using Degen"
    :return: List of result values. 
    :rtype: List[int]
    """

    # define "fluff" elements
    title_bar_row = [sg.Text(strings.get_string("roll_dice_title"))]
    description_row = [sg.Text(description, auto_size_text=True)]
    v_separator = [sg.HSeparator(pad=((0,0), (0,1)))]
    v_separator2 = [sg.HSeparator(pad=((0,0), (0,1)))]
    submit_row = [sg.Submit()]

    # create ids for GUI elements according to PySimpleGUI convention
    dice_ids = [f"-DICE{id}-" for id in list(range(0,len(dice)))]
    
    # create dice row GUI elements
    # TODO: add scroll bar if more than 20 elements
    dice_rows = []
    for i in range(len(dice)):
        dice_rows.append(get_dice_roll_line(dice_ids[i], dice[i]))

    # open window, close on next interaction
    layout = [title_bar_row, v_separator, description_row, v_separator2, dice_rows, submit_row]
    window = sg.Window(strings.get_string("roll_dice_title"), layout)
    event, values = window.read()
    window.close()

    # TODO: add input validation. ATM user can input any value
    # TODO: add proper "None" check. If UI is closed with the "X" button, all values are None --> TypeError
    try:
        return [int(values.get(key)) for key in dice_ids]
    except TypeError:
        return [False for die in dice]


if __name__ == "__main__":
    print(get_dice_rolls([20, 20, 20], "normal ability check"))
    print(get_dice_rolls([100]*100, "absolutely overloaded UI"))
