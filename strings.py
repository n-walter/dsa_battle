from typing import Dict
import config
import json

strings = False

def get_strings() -> Dict:
    touch_strings()
    return strings

def touch_strings(force_reload=False):
    global strings
    if not strings:
        with open("strings.json", "r") as source: 
            strings = json.load(source)

def get_string(string_name: str) -> str:
    try:
        return get_strings()[string_name][config.get_language_code()]
    except KeyError:
        print(f"WARNING: cannot find string {string_name} for configured language, trying default language")
        try:
            return get_strings()[string_name][config.get_default_language_code()]
        except KeyError:
            print(f"WARNING: cannot find string {string_name} for default language, setting error message")
            return f"ERROR: {string_name}"
    