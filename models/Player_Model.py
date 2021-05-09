import numpy as np

class Player:
    def __init__(self, number):
        self.player_number = number
        self.pawns_in_table = np.array([])
        self.pawns_in_base = 4
        self.pawns_in_home = 0
        self.entry_table_cell = 0
        self.last_common_cell = 0

    def new_Pawn_In_Table(self):
        self.pawns_in_table.append(self.entry_table_cell)

    def update_Pawn_In_Table(self, pawn_number, location):
        self.pawns_in_table[pawn_number] = location