from typing import Dict
import config
import json

strings = False

def get_all_strings() -> Dict:
    touch_strings()
    return strings

def touch_strings(force_reload=False):
    global strings
    if not strings:
        with open("strings.json", "r") as source: 
            strings = json.load(source)

def get_dice_string(dice_count: int, dice_sides: int, base: int = 0):
    """
    returns a roll prompt string, e.g. "3W20" or "1D6+3"
    """
    base_str = f"+{base}" if base != 0 else ""
    return f"{dice_count}{get_str("dice_char")}{dice_sides}{base_str}"

def get_str(string_name: str) -> str:
    try:
        return get_all_strings()[string_name][config.get_language_code()]
    except KeyError:
        print(f"WARNING: cannot find string {string_name} for configured language, trying default language")
        try:
            return get_all_strings()[string_name][config.get_default_language_code()]
        except KeyError:
            print(f"WARNING: cannot find string {string_name} for default language, returning error message")
            return f"ERROR: {string_name}"
    