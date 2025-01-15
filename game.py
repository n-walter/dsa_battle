from typing import Tuple

from fighter import FighterInstance
from weapon import Weapon
import strings


class Game:
    def __init__(self):
        self.fighters = []
        self.current_round = 0
        self.current_ini_index = 0

    def add_fighter(self, fighter: FighterInstance):
        """
        iterate over all currently added fighters, add new fighter
        in front of the first fighter with lower INI
        """
        for i in range(len(self.fighters)):
            if self.fighters[i] <= fighter.current_ini:
                self.fighters[i:i] = fighter
                break

    def next_fighter(self) -> Tuple[int, FighterInstance]:
        """
        increases the current ini index, setting the next fighter as "active"

        :return: tuple containing current round counter and next active fighter
        """
        # I am 99,99% this should be possible in one line but my brain refuses
        # to give me the solution. modulo would work if we didnt care about 
        # the round counter
        self.current_ini_index += 1
        if self.current_ini_index >= len(self.fighters):
            return self.next_round()
        return (self.current_round, self.fighters[self.current_ini_index])
        
    def next_round(self) -> Tuple[int, FighterInstance]:
        """
        starts the next round by resetting ini index

        :return: tuple containing current round counter and next active fighter
        """
        self.current_ini_index = 0
        self.current_round += 1
        return (self.current_round, self.fighters[self.current_ini_index])