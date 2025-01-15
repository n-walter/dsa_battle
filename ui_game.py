import PySimpleGUI as sg

from fighter import FighterInstance
from weapon import Weapon
import strings

def get_fighter_ui_frame(fighter: FighterInstance) -> sg.Frame:
    """
    returns this fighter instance's UI frame (for display in lists, e.g. the initative bar)
    """
    top_row = [sg.Push(), sg.Text(f"INI {fighter.current_ini} | #{fighter.ini_position}")]
    lep_row = [sg.Text(f"{fighter.current_lep}/{fighter.max_lep} {strings.get_str("LeP_short")}"), 
                sg.Push(),
                sg.Text(f"{fighter.pain} {strings.get_str("pain_word")}")]
    melee_frame = sg.Frame(strings.get_str("melee_weapons"), layout=[[get_weapon_ui_frame(w) for w in fighter.melee_weapons]])
    
    ranged_frame = sg.Frame(strings.get_str("range_weapons"), layout=[[get_weapon_ui_frame(w) for w in fighter.ranged_weapons]])

    layout = [top_row, lep_row, [[melee_frame]], [[ranged_frame]]]
    return sg.Frame(fighter.instance_name, layout)

def get_weapon_ui_frame(weapon: Weapon, AT: int = 0, PA: int = 0) -> sg.Frame:
    name_str = weapon.name

    if weapon.simple:
        AT = weapon.AT
        PA = weapon.PA
    else:
        AT = AT + weapon.AT_modifier
        PA = PA + weapon.PA_modifier

    tp_str = f"{strings.get_str("TP_short")}: {strings.get_dice_string(weapon.tp_dice["count"], weapon.tp_dice["sides"], weapon.tp_base)}"
    rw_short = strings.get_str("RW_short")
    rw_str = f"{rw_short}: {strings.get_str("range_names")[weapon.range]}" if weapon.type == "melee" else f"{rw_short}: {'/'.join([str(r) for r in weapon.range])}"
    at_or_fk = strings.get_str("AT_short") if weapon.type == "melee" else strings.get_str("FK_short")
    at_str = f"{at_or_fk}: {AT}"
    pa_str = f"{strings.get_str("PA_short")}: {PA}" if weapon.type == "melee" else ""

    layout = [[sg.Text(tp_str), sg.Push(), sg.Text(rw_str), sg.Push(), sg.Text(at_str), sg.Push(), sg.Text(pa_str)]]

    return sg.Frame(name_str, layout)