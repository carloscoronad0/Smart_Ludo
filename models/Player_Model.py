import numpy as np

class Player:
    def __init__(self, number):
        self.player_id = number # Id for identifying the player

        # To keep track of the pawns of the player 
        self.pawns_in_table = []
        self.pawns_in_base = 4
        self.pawns_in_home = 0

        # Cells that indicate the begining and the end for a pawn in the common table
        self.entry_table_cell = 0
        self.last_common_cell = 0

    def new_Pawn_In_Table(self):
        self.pawns_in_base -= 1
        self.pawns_in_table.append(self.entry_table_cell)
        return len(self.pawns_in_table) - 1

    def update_Pawn_In_Table(self, pawn_number, location):
        self.pawns_in_table[pawn_number] = location

    def pawn_in_home(self, pawn_number):
        self.pawns_in_home += 1
        self.pawns_in_table[pawn_number] = -6