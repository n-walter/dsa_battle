import json
import PySimpleGUI as sg

from constants import MELEE_RANGE_INTS
import config


class Weapon:
    def __init__(self, file: str) -> None:
        with open(file) as source:
            self.data = json.load(source)
        
        self.simple = self.data["simple"]
        self.type = self.data["type"]
        self.technique = self.data["technique"]
        self.name = self.data["name"][config.get_language_code()]
        
        
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

    def get_ui_frame(self) -> sg.Frame:
        temp_layout = [sg.Text(f"{self.type}")]
        return sg.Frame(f"temp weapon frame{self.type}", temp_layout)

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
    

def get_weapon_by_file_name(file_name:str) -> Weapon:
    folder = config.get_folders()["weapons"]
    return Weapon(f"{folder}/{file_name}")