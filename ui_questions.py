import PySimpleGUI as sg
from typing import List, Any, Tuple

import config
import strings                  # translations
from constants import MELEE_RANGE_INTS


class ComboHelper:
    def __init__(self, value: Any, show_str: str) -> None:
        self.value = value
        self.show_str = show_str

    def __repr__(self) -> str:
        return f"self.show_str ({self.value})"


def get_enemy_melee_range(target) -> int:
    # TODO: umbauen auf get_multiple_modfiers_window()
    local_prompt_string = strings.get_str("give_enemy_melee_range_prompt")
    prompt_string = f"{local_prompt_string}: {target.instance_name}"
    
    # define "fluff" elements
    title_bar_row = [sg.Text(prompt_string)]
    v_separator = [sg.HSeparator(pad=((0,0), (0,1)))]
    submit_row = [sg.Submit()]

    input_text = f"{strings.get_str("range_string")}: "
    default_value = config.get_default_melee_range()

    # TODO: implement selection for enemy weapons in addition to manual input
    input_key = "-MANUAL RANGE-"

    # TODO: switch to Combo instead of InputText
    range_row = [sg.Text(input_text, size=(25,1)), sg.VSeparator(pad=((10,0),(0,0))), sg.InputText(key=input_key, size=(5,1), default_text=default_value)]

    # open window, close on next interaction
    layout = [title_bar_row, v_separator, range_row, submit_row]
    window = sg.Window(strings.get_str("give_enemy_melee_range_prompt"), layout, resizable=True)
    event, values = window.read()
    window.close()

    try:
        return MELEE_RANGE_INTS[values.get(input_key)]
    except KeyError:
        return get_enemy_melee_range


def get_multiple_modfiers_window(description: str, modifiers: List[Tuple[str, ComboHelper, List[ComboHelper]]]) -> sg.Window:
    """
    creates a window object for multiple modifiers
    """
    # TODO
    title_bar_row = [sg.Text(description)]
    v_separator = [sg.HSeparator(pad=((0,0), (0,1)))]
    submit_row = [sg.Submit()]

    modifiers_rows = [sg.Text(desc), sg.Combo()]

def get_ranged_modifier(weapon, shooter, target):
    modifiers_distance = [
        ComboHelper(-2, f"{weapon.range["medium"]}-{weapon.range["long"]}"),
        ComboHelper(0, f"{weapon.range["short"]}-{weapon.range["medium"]}"),
        ComboHelper(2, f"0-{weapon.range["short"]}")
    ]
    modifiers_distance_desc = strings.get_str("range_selector_prompt")
    modifiers_distance_default = modifiers_distance[1]
    modifiers_distance_tuple = (modifiers_distance_desc, modifiers_distance_default, modifiers_distance)

    size_strings = strings.get_str("creature_size_strings")
    modifiers_enemy_size = [
        ComboHelper(-8, size_strings["tiny"]),
        ComboHelper(-4, size_strings["small"]),
        ComboHelper(0, size_strings["medium"]),
        ComboHelper(4, size_strings["large"]),
        ComboHelper(8, size_strings["giant"])
    ]
    modifiers_enemy_size_desc = strings.get_str("enemy_size_selector_prompt")
    modifiers_enemy_size_default = modifiers_enemy_size[2]
    modifiers_enemy_size_tuple = (modifiers_enemy_size_desc, modifiers_enemy_size_default, modifiers_enemy_size)

    movement_strings = strings.get_str("movement_speeds")
    modifiers_target_movement = [
        ComboHelper(-2, movement_strings["fast"]),
        ComboHelper(0, movement_strings["slight"]),
        ComboHelper(2, movement_strings["still"])
    ]
    modifiers_target_movement_desc = strings.get_str("enemy_movement_selector_prompt")
    modifiers_target_movement_default = modifiers_target_movement[1]
    modifiers_target_movement_tuple = () # TODO current work is HERE

    modifiers_target_dodging = [
        ComboHelper(-4, movement_strings["dodging"]),
        ComboHelper(0, movement_strings["not_dodging"])
    ]

    modfiers_shooter_movement = [
        ComboHelper(-4, movement_strings["fast"]),
        ComboHelper(-2, movement_strings["slight"]),
        ComboHelper(0, movement_strings["still"])
    ]

    visibility_strings = strings.get_str("visibility")
    modifiers_visibility = [
        ComboHelper(-999, visibility_strings["invisible"]),
        ComboHelper(-6, visibility_strings["level_3"]),
        ComboHelper(-4, visibility_strings["level_2"]),
        ComboHelper(-2, visibility_strings["level_1"]),
        ComboHelper(0, visibility_strings["clear"])
    ]

    horse_strings = strings.get_str("movement_speeds_horse")
    modifiers_horse = [
        ComboHelper(-999, horse_strings["level_2"]),
        ComboHelper(-8, horse_strings["level_3"]),
        ComboHelper(-4, horse_strings["level_1"]),
        ComboHelper(0, horse_strings["level_0"]),
    ]

    getuemmel_strings = strings.get_str("shooting_into_melee")
    modifiers_getuemmel = [
        ComboHelper(-2, getuemmel_strings["yes"]),
        ComboHelper(0, getuemmel_strings["no"])
    ]