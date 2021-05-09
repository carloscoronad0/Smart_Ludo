import numpy as np
from tqdm import tqdm
import Player_Model

common_table_size = 52
last_cells = 5

class Ludo_Game:
    def __init__(self, number_of_players):
        self.number_of_players = number_of_players
        self.ludo_table = np.zeros(common_table_size)
        self.last_cells = np.array([np.zeros(last_cells) for i in range(number_of_players)])
        self.dice = 0
        self.players = np.array([Player_Model.Player(i+1) for i in range(number_of_players)])

    def set_To_Start(self):
        for i in range(self.number_of_players):
            entry_cell = i * 13
            last_common_cell = (entry_cell + common_table_size - 2) % common_table_size

            self.players[i].entry_table_cell = entry_cell
            self.players[i].last_common_cell = last_common_cell

    def roll_Dice(self):
        self.dice = np.random.randint(1,7)

    def put_Pawn_In_Table(self, player_number):
        self.ludo_table[self.players[player_number].entry_table_cell] = player_number

    def advance_In_Table(self, player_number, pawn_number):
        actual_location = self.players[player_number].pawns_in_table[pawn_number]
        new_location = actual_location + self.dice
        eaten_player = 0

        # if in the table, the value allocated  in the new location 
        # calculated for the pawn is greater than 0, then there's another 
        # pawn in that location
        if self.ludo_table[new_location] > 0:
            eaten_player = self.ludo_table[new_location]
        
        self.ludo_table[actual_location] = 0
        self.ludo_table[new_location] = player_number

        return eaten_player