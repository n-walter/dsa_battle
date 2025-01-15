import json
import PySimpleGUI as sg

from constants import MELEE_RANGE_INTS
import config
import strings


class Weapon:
    def __init__(self, file: str) -> None:
        with open(file) as source:
            self.data = json.load(source)
        
        self.simple = self.data["simple"]
        self.type = self.data["type"]
        self.technique = self.data["technique"]
        self.name = self.data["name"][config.get_language_code()]
        
        # set range
        if self.type == "melee":
            self.range = MELEE_RANGE_INTS[self.data["range"]]
        if self.type == "ranged":
            self.range = self.data["range"]

        # set loading for ranged weapons
        if self.type == "ranged":
            self.loading_time = self.data["loading_time"]
            self.loading_state = self.loading_time # we assume fights start with prepared weapons

        # set AT/PA if simple, modifiers if not
        if self.simple:
            self.AT = self.data["AT"]
            self.PA = self.data["PA"]
        else:
            if self.type == "melee":
                self.AT_modifier = self.data["modifiers"]["AT"]
                self.PA_modifier = self.data["modifiers"]["PA"]
            else: 
                self.AT_modifier = 0
                self.PA_modifier = 0

        self.tp_base = self.data["TP"]["hard"]
        self.tp_dice = self.data["TP"]["dice"][0]

    def get_remaining_loading_time(self) -> int:
        return self.loading_time - self.loading_state
    
    def load(self, amount: int = 1) -> int:
        self.loading_state += amount
        if self.loading_state > self.loading_time:
            self.loading_state = self.loading_time
        return self.get_remaining_loading_time()

    def unload(self) -> int:
        self.loading_state = 0
        return self.get_remaining_loading_time()
    
    def calculate_damage(self) -> int:
        # TODO
        return NotImplementedError
    

def get_weapon_by_file_name(file_name:str) -> Weapon:
    folder = config.get_folders()["weapons"]
    return Weapon(f"{folder}/{file_name}")


def example_weapon_frame():
    melee_weapon = get_weapon_by_file_name("dagger.json")
    melee_weapon2 = get_weapon_by_file_name("mage_staff_short.json")
    range_weapon = get_weapon_by_file_name("kurzbogen.json")
    test_layout = [[melee_weapon.get_ui_frame(AT=16, PA=8)], [melee_weapon2.get_ui_frame()], [range_weapon.get_ui_frame()]]
    test_window = sg.Window("testing weapon layout", test_layout, resizable=True)
    event, values = test_window.read()
    test_window.close()
    pass


if __name__ == "__main__":
    example_weapon_frame()