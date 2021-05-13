import numpy as np

PUT_PAWN_ON_TABLE = 1
MOVE_PAWN = 2
PUT_PAWN_ON_TABLE_ACTION = (-1, None, PUT_PAWN_ON_TABLE)

def adapt_State(ludo_game, number_of_pawn_moves, player_number, possible_moves):

    print("Moves on adapt: ", possible_moves)
    if number_of_pawn_moves == 1:
        pn1, _, _ = possible_moves[0]
        state = (ludo_game.get_Pawn_State(player_number,pn1))

    if number_of_pawn_moves == 2:
        pn1, _, _ = possible_moves[0]
        pn2, _, _ = possible_moves[1]
        state = (ludo_game.get_Pawn_State(player_number, pn1), ludo_game.get_Pawn_State(player_number, pn2))
                                    
    elif number_of_pawn_moves == 3:
        pn1, _, _ = possible_moves[0]
        pn2, _, _ = possible_moves[1]
        pn3, _, _ = possible_moves[2]
        state = (ludo_game.get_Pawn_State(player_number, pn1), ludo_game.get_Pawn_State(player_number, pn2), 
            ludo_game.get_Pawn_State(player_number, pn3))

    elif number_of_pawn_moves == 4:
        pn1, _, _ = possible_moves[0]
        pn2, _, _ = possible_moves[1]
        pn3, _, _ = possible_moves[2]
        pn4, _, _ = possible_moves[3]
        state = (ludo_game.get_Pawn_State(player_number, pn1), ludo_game.get_Pawn_State(player_number, pn2), 
            ludo_game.get_Pawn_State(player_number, pn3), ludo_game.get_Pawn_State(player_number, pn4))

    return state

def get_Possible_Moves_Analized(possible_moves, can_Put_Pawn_In_Table):
    possible_moves_substracted = possible_moves.copy()

    if can_Put_Pawn_In_Table:
        possible_moves_substracted.remove(PUT_PAWN_ON_TABLE_ACTION)

    return (possible_moves, possible_moves_substracted, len(possible_moves_substracted))

def display_Pawn_Options(options):

    for i in range(len(options)):
        if options[i][2] == MOVE_PAWN:
            print(f"{i}.- Move pawn {options[i][0]} in location {options[i][1]}")
        else:
            print(f"{i}.- Put pawn on table")

def get_Player_Decision(player_id, action_desired, possible_options):
    player_decision = ""
    while possible_options.__contains__(player_decision) is not True:
        print(f"Player {player_id}, {action_desired}")
        player_decision = input()

    return int(player_decision)

def display_Table_For_User(ludo_table, last_cells):
    split_table = np.split(ludo_table, 4, axis=0)
    tab = "\t"
    tabulations = tab

    for i in range(4):
        print(f"{tabulations}{split_table[i]}")
        tabulations += tab

    for i in range(len(last_cells)):
        print(f"\tCell {i}: {last_cells[i]}")