from typing import Self, Any, List, Dict

import json

import ui_dice
import strings

class Weapon:
    def __init__(self, file: str) -> None:
        with open(file) as source:
            self.data = json.load(source)
        
        self.simple = self.data["simple"]
        self.type = self.data["type"]
        self.technique = self.data["technique"]

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


class FighterInstance:
    def __init__(self, fighter_type: Fighter) -> None:
        self.fighter_type = fighter_type
        self.current_lep = self.fighter_type.lep
        self.current_ini = ui_dice.get_dice_rolls([6], strings.get_string("roll_ini_prompt"))[0] + self.fighter_type.ini

    def try_melee_attack(self, weapon: Weapon) -> bool:
        if weapon.simple:
            target_at = weapon.at
        else:
            target_at = self.fighter_type.fighting[weapon.technique] + weapon.at_modifier

        prompt_string = f"{strings.get_string("roll_attack_prompt")} ({target_at})"

        return ui_dice.get_dice_rolls([20], prompt_string)[0] <= target_at
        
        
    
    def attack(self, target: Self, weapon: Weapon):
        pass

