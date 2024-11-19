from typing import Self, Any, List, Dict

import json

import ui_dice
import ui_questions
import strings
import config

from constants import MELEE_RANGE_INTS
from calculations import calculate_range_at_advantage






class Weapon:
    def __init__(self, file: str) -> None:
        with open(file) as source:
            self.data = json.load(source)
        
        self.simple = self.data["simple"]
        self.type = self.data["type"]
        self.technique = self.data["technique"]
        
        self.range = MELEE_RANGE_INTS[self.data["range"]]

        if self.simple:
            self.at = self.data["AT"]
        else:
            self.at_modifier = self.data["modifiers"]["AT"]
            self.pa_modifier = self.data["modifiers"]["PA"]


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
    def __init__(self, fighter_type: Fighter) -> None:
        self.fighter_type = fighter_type
        self.current_lep = self.fighter_type.lep
        self.current_ini = ui_dice.get_dice_rolls([6], strings.get_string("roll_ini_prompt"))[0] + self.fighter_type.ini

        self.instance_name = fighter_type.name

    def try_melee_attack(self, weapon: Weapon, enemy: Self) -> bool:
        if weapon.simple:
            target_at = weapon.at
        else:
            target_at = self.fighter_type.fighting[weapon.technique] + weapon.at_modifier

        # get weapon range (dis)advantage
        own_range = weapon.range
        enemy_range = ui_questions.get_enemy_melee_range(enemy)
        range_advantage = calculate_range_at_advantage(own_range, enemy_range)
        print(f"range_advantage: {range_advantage}")

        target_at += range_advantage

        prompt_string = f"{strings.get_string("roll_attack_prompt")} ({target_at})"

        return ui_dice.get_dice_rolls([20], prompt_string)[0] <= target_at
    
    def try_ranged_attack(self, weapon: Weapon) -> bool:
        raise NotImplementedError
        if weapon.simple:
            target_at = weapon.at
        else:
            target_at = self.fighter_type.fighting[weapon.technique] + weapon.at_modifier

    def try_parry(self, weapon: Weapon) -> bool:
        raise NotImplementedError

    def try_dodge(self, modifier: int) -> bool:
        raise NotImplementedError
        

