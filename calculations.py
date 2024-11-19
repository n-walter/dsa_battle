def calculate_range_at_advantage(attacker_range: int, defender_range: int) -> int:
    # range ints defined in constants.py
    # --> each advantage "level" gives a modifier of two.
    
    diff = defender_range - attacker_range
    if diff < 0:
        diff = 0
    return diff * 2