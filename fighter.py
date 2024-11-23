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
        
        
        if self.type == "melee":
            self.range = MELEE_RANGE_INTS[self.data["range"]]
        if self.type == "ranged":
            self.range = self.data["range"]

            self.loading_time = self.data["loading_time"]
            self.loading_state = self.loading_time # we assume fights start with prepared weapons

        if self.simple:
            self.at = self.data["AT"]
        else:
            if self.type == "melee":
                self.at_modifier = self.data["modifiers"]["AT"]
                self.pa_modifier = self.data["modifiers"]["PA"]
            else: 
                self.at_modifier = 0
                self.pa_modifier = 0

    def get_remaining_loading_time(self) -> int:
        return self.loading_time - self.loading_state
    
    def load(self, amount: int = 1) -> int:
        self.loading_state += amount
        if self.loading_state > self.loading_time:
            self.loading_state = self.loading_time
        return self.get_remaining_loading_time()

    def unload(self):
        self.loading_state = 0
        return self.get_remaining_loading_time()


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
        self.instance_name = fighter_type.name
        self.current_lep = self.fighter_type.lep

        roll_ini_prompt = f"{strings.get_string("roll_ini_prompt")}: {self.instance_name}"
        self.current_ini = ui_dice.get_dice_rolls([6], roll_ini_prompt)[0] + self.fighter_type.ini


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

        target_at += range_advantage

        prompt_string = f"{strings.get_string("roll_attack_prompt")} ({target_at})"

        roll = ui_dice.get_dice_rolls([20], prompt_string)[0]
        success = roll <= target_at
        # TODO: if crit: automatic fail or hit, no matter what the target was
        if success:
            crit = roll == 1
        else:
            crit = roll == 20

        return (success, crit)
    
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
        if weapon.simple:
            target_at = weapon.at
        else:
            target_at = self.fighter_type.fighting[weapon.technique] + weapon.at_modifier



        


        
        
    def try_parry(self, weapon: Weapon) -> bool:
        raise NotImplementedError

    def try_dodge(self, modifier: int) -> bool:
        raise NotImplementedError
        

