from typing import Dict
import json

config = False

def get_config() -> Dict:
    touch_config()
    return config

def touch_config(force_reload=False):
    global config
    if not config:
        with open("config.json", "r") as source: 
            config = json.load(source)

def get_language_code() -> str:
    return get_config()["language"]

def get_default_language_code() -> str:
    return get_config()["default_language"]

def get_default_melee_range() -> str:
    return get_config()["default_melee_range"]