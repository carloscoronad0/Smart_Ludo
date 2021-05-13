from models import Player_Model
import numpy as np

# Table dimensions
COMMON_TABLE_SIZE = 52
LAST_CELLS = 5

# Identifiers for actions
PUT_PAWN_ON_TABLE = 1
MOVE_PAWN = 2

class Ludo_Game:
    def __init__(self):
        self.number_of_players = 0
        self.ludo_table = [] # The common table, where all the players can interact
        self.last_cells = [] # The last 5 cells each color has only for them
        self.dice = 0
        self.players = [] # The list of players participating on the game
        self.unavailable_eating_cells = [] # Cells were eating another player isn't possible

    # ------------------------------------------------------------------------------------------------------------------------------
    # SETUP FUNCTIONS --------------------------------------------------------------------------------------------------------------

    def initialize(self, number_of_players): # Initialize function for setting up everything in the game
        self.number_of_players = number_of_players
        self.ludo_table = np.zeros(COMMON_TABLE_SIZE)
        self.last_cells = np.array([np.zeros(LAST_CELLS) for i in range(number_of_players)])
        self.dice = 0
        self.players = np.array([Player_Model.Player(i+1) for i in range(number_of_players)])

        self.set_To_Start()

    def set_To_Start(self):
        # Set some last details necessary to start the game, the index of the starting cell and the last 
        # cell in the common table
        for i in range(self.number_of_players):
            entry_cell = i * 13
            last_common_cell = (entry_cell + COMMON_TABLE_SIZE - 2) % COMMON_TABLE_SIZE

            self.players[i].entry_table_cell = entry_cell
            self.players[i].last_common_cell = last_common_cell

            self.unavailable_eating_cells.append(entry_cell)


    # ------------------------------------------------------------------------------------------------------------------------------
    # GAME VERIFICATIONS -----------------------------------------------------------------------------------------------------------

    def can_Enter_Last_Cells(self, last_common_cell, current_location, target_location):
        print("Can enter: ", (current_location <= last_common_cell) & (target_location > last_common_cell))
        return (current_location <= last_common_cell) & (target_location > last_common_cell)

    def game_Done(self, player_number):
        return self.players[player_number].pawns_in_home == 4

    # ------------------------------------------------------------------------------------------------------------------------------
    # GAME FUNCTIONS ---------------------------------------------------------------------------------------------------------------

    def roll_Dice(self):
        self.dice = np.random.randint(1,7) # Dice number from 1-6
        print(self.ludo_table)

    def put_Pawn_In_Table(self, player_number):
        # Setting player id on the entry cell into the ludo table
        self.ludo_table[self.players[player_number].entry_table_cell] = self.players[player_number].player_id
        return self.players[player_number].new_Pawn_In_Table()

    def can_Put_Pawn_In_Table(self, player_number):
        # If the player can put one more pawn in Table
        print("Can put pawn in table: ", (self.players[player_number].pawns_in_base > 0) & (self.dice == 6))
        return (self.players[player_number].pawns_in_base > 0) & (self.dice == 6)

    def pawn_Has_Been_Eaten(self, player_number, location):
        self.players[player_number].pawn_Eaten(location)

    def get_Pawn_State(self, player_number, pawn_number):
        # Returns the next six cells from a pawn represented in a number
        location = self.players[player_number].pawns_in_table[pawn_number]
        last_common_cell = self.players[player_number].last_common_cell
        id = self.players[player_number].player_id
        value = 0

        if location >= 0: # If location is positive then the pawn is still in the common table
            if (location + 6) > last_common_cell: # Verify if it's possible that the pawn enters the last cells
                max_value = 7 - ((location + 6) % last_common_cell)
            else:
                max_value = 7
            
            for i in range(1,max_value):
                advancing_location = (location + i) % COMMON_TABLE_SIZE
                if (self.ludo_table[advancing_location] > 0) & (self.ludo_table[advancing_location] != id):
                    value += 2**(i-1)
                    print("Value: ", value)

        else:
            value = 2**(6 + location)

        return value

    def advance_In_Table(self, player_number, pawn_number):

        current_location = self.players[player_number].pawns_in_table[pawn_number]
        print("\tCurrent location: ", current_location)
        consecuence = (0, -1)

        if current_location >= 0: # Pawn is still on common table

            # Verifying if the pawn has entered the last 5 cells
            if self.can_Enter_Last_Cells(self.players[player_number].last_common_cell, current_location, (current_location + self.dice)):
                print("Entering last cells")
                new_location = (current_location + self.dice) % self.players[player_number].last_common_cell
                print("\tNew location: ", new_location)

                # If new_location is 6 then it enters home directly
                if new_location == 6:
                    self.players[player_number].pawn_in_home(pawn_number)
                    consecuence = (-1, -1)
                else: # else it enters into the last cells
                    self.last_cells[player_number][new_location - 1] = self.players[player_number].player_id
                    print("\tLast cells: ", self.last_cells)
                    self.players[player_number].update_Pawn_In_Table(pawn_number, new_location * (-1))
                    
            else:
                print("Continue in common cells")
                new_location = (current_location + self.dice) % COMMON_TABLE_SIZE
                print("\tNew location: ", new_location)

                # if in the table, the value allocated  in the new location 
                # calculated for the pawn is greater than 0, then there's another 
                # pawn in that location
                if self.ludo_table[new_location] > 0 & self.unavailable_eating_cells.__contains__(new_location) is not True:
                    consecuence = (self.ludo_table[new_location], new_location)

                self.ludo_table[new_location] = self.players[player_number].player_id
                self.players[player_number].update_Pawn_In_Table(pawn_number, new_location)
                
            self.ludo_table[current_location] = 0

        else: # else the Pawn is in the last cells

            new_location = abs(current_location) + self.dice
            print("\tNew location: ", new_location)

            if new_location == 6: # If new_location is 6 then the pawn has reached home
                self.players[player_number].pawn_in_home(pawn_number)
                consecuence = (-1, -1)

            else:
                self.last_cells[player_number][new_location - 1] = self.players[player_number].player_id
                self.players[player_number].update_Pawn_In_Table(pawn_number, new_location * (-1))

            self.last_cells[player_number][abs(current_location + 1)] = 0 # Is plus 1 because current_location is negative

        return consecuence

    # Get the possible moves the player can perform with his pawns
    def get_Possible_Moves(self, player_number):
        print("Getting possible moves--------------")
        possible_moves = []

        for i in range(len(self.players[player_number].pawns_in_table)):
            current_location = self.players[player_number].pawns_in_table[i]
            print(f"\tPawn {i} current location {current_location}")

            if current_location >= 0: # if it's positive then the pawn is in the common table
                possible_location = (current_location + self.dice) % COMMON_TABLE_SIZE
                print(f"\t\tPawn {i} Possible location: ", possible_location)

                if self.can_Enter_Last_Cells(self.players[player_number].last_common_cell, current_location, current_location + self.dice):
                    possible_moves.append((i, current_location, MOVE_PAWN))

                elif self.ludo_table[possible_location] != self.players[player_number].player_id:  
                    # (Pawn number, Pawn position, Action)
                    possible_moves.append((i, current_location, MOVE_PAWN))

            elif abs(current_location) < 6: # else the pawn is in the last cells
                possible_location = abs(current_location - self.dice)
                print(f"\t\tPawn {i} Possible location: ", possible_location)

                if possible_location <= 6: # Pos 6 is home
                    # (Pawn number, Pawn position, Action)
                    possible_moves.append((i, current_location, MOVE_PAWN))
                    print("\t\tAppended")

        if self.can_Put_Pawn_In_Table(player_number):
            # (Pawn number, Pawn position, Action)
            possible_moves.append((-1, None, PUT_PAWN_ON_TABLE))

        return possible_moves