from typing import Tuple, List

def calculate_range_at_advantage(attacker_range: int, defender_range: int) -> int:
    # range ints defined in constants.py
    # --> each advantage "level" gives a modifier of two.
    
    diff = defender_range - attacker_range
    if diff < 0:
        diff = 0
    return diff * 2

def check_hit_and_crit(target_at: int, roll: int, crit_success: int = 1, crit_fail: int = 20) -> Tuple[bool, bool]:
    if roll == crit_success:
        return (True, True)
    elif roll == crit_fail:
        return (False, True)
    else:
        return (roll <= target_at, False)
    
def check_ability(fighter, description: str, stat_types: List[str], skill_value: int = 0) -> bool:
    # TODO: skill value can be got from fighter object
    # TODO: implement Erschwernis/ Erleichterung
    return False
