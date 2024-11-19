import PySimpleGUI as sg
from typing import List, Dict, Any, Self, Set

import config
import strings                  # translations
from constants import MELEE_RANGE_INTS


def get_enemy_melee_range(target) -> int:
    local_prompt_string = strings.get_string("give_enemy_melee_range_prompt")
    prompt_string = f"{local_prompt_string}: {target.instance_name}"
    
    # define "fluff" elements
    title_bar_row = [sg.Text(prompt_string)]
    v_separator = [sg.HSeparator(pad=((0,0), (0,1)))]
    submit_row = [sg.Submit()]

    input_text = f"{strings.get_string("range_string")}: "
    default_value = config.get_default_melee_range()

    # TODO: implement selection for enemy weapons in addition to manual input
    input_key = "-MANUAL RANGE-"
    range_row = [sg.Text(input_text, size=(25,1)), sg.VSeparator(pad=((10,0),(0,0))), sg.InputText(key=input_key, size=(5,1), default_text=default_value)]

    # open window, close on next interaction
    layout = [title_bar_row, v_separator, range_row, submit_row]
    window = sg.Window(strings.get_string("give_enemy_melee_range_prompt"), layout, resizable=True)
    event, values = window.read()
    window.close()

    try:
        return MELEE_RANGE_INTS[values.get(input_key)]
    except KeyError:
        return get_enemy_melee_range


def get_ranged_parameters():
    modifier_distance = 0
    # get ranged parameters
    # close: +2
    # middle: +0
    # far: -2

    modifier_size = 0
    # get size parameters
    # tiny: -8
    # small: -4
    # medium: +0
    # large: +4
    # huge: +8

    modifier_moving_target = 0
    modifier_moving_target_dodging = -4
    # get moving parameters
    # target standing still: +2
    # target slight movement: +0
    # target fast movement: -2

    modifier_moving_shooter = 0
    # shooter moving: -2
    # shooter running: -4