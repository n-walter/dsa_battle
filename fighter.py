from typing import Self, Any, List, Dict
import PySimpleGUI as sg

import json

import ui_dice
import ui_questions
import strings
import config

from constants import MELEE_RANGE_INTS
from calculations import calculate_range_at_advantage, check_hit_and_crit, check_ability
from weapon import Weapon, get_weapon_by_file_name


class Fighter:
    def __init__(self, file: str):
        with open(file) as source:
            self.data = json.load(source)
        self.lep = self.data["properties"]["basics"]["LeP"]
        self.ini = self.data["properties"]["basics"]["INI"]
        self.fighting = self.data["properties"]["fighting"]
        try: 
            self.name = self.data["name"][config.get_language_code()]
        except KeyError:
            try: 
                self.name = self.data["name"][config.get_default_language_code()]
            except KeyError:
                self.name = "NAME_ERROR"
        

class FighterInstance:
    def __init__(
            self, 
            fighter_type: Fighter, 
            name_suffix: str = None,
            current_lep: int = None,
            current_ini: int = None,
            ini_position: int = None
        ) -> None:

        self.fighter_type = fighter_type
        self.instance_name = fighter_type.name + name_suffix if name_suffix else fighter_type.name

        # set up all things related to INI
        if current_ini:
            self.current_ini = current_ini
        else:
            roll_ini_prompt = f"{strings.get_string("roll_ini_prompt")}: {self.instance_name}"
            self.current_ini = ui_dice.get_dice_rolls([6], roll_ini_prompt)[0] + self.fighter_type.ini
        self.ini_position = ini_position if ini_position else -1

        # set up all things related to LeP
        self.max_lep = self.fighter_type.lep
        self.current_lep = current_lep if current_lep else self.fighter_type.lep
        self.pain = self.calculate_pain()
        self.fainted = self.calculate_faint()

        # load weapons as objects
        self.melee_weapons = [get_weapon_by_file_name(weapon["file_name"]) for weapon in self.fighter_type.data["weapons"]["melee"]]
        self.ranged_weapons = [get_weapon_by_file_name(weapon["file_name"]) for weapon in self.fighter_type.data["weapons"]["ranged"]]

    def get_ui_frame(self) -> sg.Frame:
        """
        returns this fighter instance's UI frame (for display in lists, e.g. the initative bar)
        """
        top_row = [sg.Push(), sg.Text(f"INI {self.current_ini} | #{self.ini_position}")]
        lep_row = [sg.Text(f"{self.current_lep}/{self.max_lep} {strings.get_string("LeP_short")}"), 
                   sg.Push(),
                   sg.Text(f"{self.pain} {strings.get_string("pain_word")}")]
        melee_row = [sg.Text(f"melee weapons: {", ".join([weapon.name for weapon in self.melee_weapons])}")]
        ranged_row = [sg.Text(f"ranged weapons: {", ".join([weapon.name for weapon in self.ranged_weapons])}")]

        layout = [top_row, lep_row, [], melee_row, ranged_row]
        return sg.Frame(self.instance_name, layout)

    def receive_damage(self, damage_amount: int, damage_type: str = "physical", ignore_armor: bool = False) -> bool:
        # return True if killed, False if survived
        # calculate against armor, check damamage type
        self.calculate_pain()
        self.calculate_faint()
        raise NotImplementedError

    def calculate_pain(self) -> int:
        # compare current LeP against max LeP
        # return current pain level
        # TODO
        return 0
    
    def calculate_faint(self) -> bool:
        # check if current_lep <= 5
        # roll for Selbstbeherrschung
        # TODO
        selbstb = check_ability(self, "TODO: descr", ["MU", "MU", "KO"], self.fighter_type.data["properties"]["talents"].get("Körperbeherrschung", 0))
        return False

    def try_attack(self, weapon: Weapon, enemy: Self) -> bool:
        if weapon.type == "melee":
            return self.try_melee_attack(weapon, enemy)
        elif weapon.type == "ranged":
            return self.try_ranged_attack(weapon, enemy)
        else:
            raise NotImplementedError(f"attack roles for weapon type {weapon.type} not implemented")

    def try_melee_attack(self, weapon: Weapon, enemy: Self) -> bool:
        """
        collects data for and carries out a melee attack roll for this fighter with the 
        selected weapon against the selected enemy

        returns tuple of bools for result:
        (bool1, bool2)
        where bool1 is a flag for hit / miss
        bool2 is a flag for a crit hit / miss

        e.g.:
        normal hit: (True, False)
        crit hit: (True, True)
        normal miss: (False, False)
        crit miss: (False, True)
        """
        if weapon.simple:
            target_at = weapon.at
        else:
            target_at = self.fighter_type.fighting[weapon.technique] + weapon.at_modifier

        # get weapon range (dis)advantage
        own_range = weapon.range
        enemy_range = ui_questions.get_enemy_melee_range(enemy)
        range_advantage = calculate_range_at_advantage(own_range, enemy_range)
        print(f"range_advantage: {range_advantage}")

        # roll die
        target_at += range_advantage
        prompt_string = f"{self.instance_name}: {strings.get_string("roll_attack_prompt")} ({target_at})"
        roll = ui_dice.get_dice_rolls([20], prompt_string)[0]
        
        return check_hit_and_crit(target_at, roll)

    def try_ranged_attack(self, weapon: Weapon, enemy: Self) -> bool:
        """
        collects data for and carries out a ranged attack roll for this fighter with the 
        selected weapon against the selected enemy

        assumes that the weapon is correctly loaded, check beforehand

        returns tuple of bools for result:
        (bool1, bool2)
        where bool1 is a flag for hit / miss
        bool2 is a flag for a crit hit / miss

        e.g.:
        normal hit: (True, False)
        crit hit: (True, True)
        normal miss: (False, False)
        crit miss: (False, True)
        """
        raise NotImplementedError

    def try_parry(self, weapon: Weapon) -> bool:
        raise NotImplementedError

    def try_dodge(self, modifier: int) -> bool:
        raise NotImplementedError
        

def example_fighter_frame():
    f_type = Fighter("fighters/bandit.json")
    fighter = FighterInstance(f_type, name_suffix="#1", current_ini=10, ini_position=0)
    test_layout = [[fighter.get_ui_frame()]]
    test_window = sg.Window("testing fighter frame layout", test_layout, resizable=True)
    event, values = test_window.read()
    test_window.close()


if __name__ == "__main__":
    example_fighter_frame()