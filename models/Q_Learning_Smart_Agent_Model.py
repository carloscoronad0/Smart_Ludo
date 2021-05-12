import numpy as np
from tqdm import tqdm
import pickle
import time

class QL_Smart_Agent:
    def __init__(self, paths):
        # The model is designed to use multiple tables, since the decision it may take may depend on the number of pawns
        # it has on the table board
        self.q_tables = [None, None, None]
        self.load_Q_Tables(paths)

    # ------------------------------------------------------------------------------------------------------------------------------
    # TABLE MANAGING ---------------------------------------------------------------------------------------------------------------

    def load_Q_Tables(self, paths):
        if len(paths) == len(self.q_tables): # There are 3 Q-Tables the agent is going to use
            print("##Loading paths##")

            for i in range(3):   # includes 2 and excludes 3, Q -Tables are only necessary when the agent has 2-4 pawns on the table
                if paths[i] is None: # If there's no path the agent creates a new table 
                    self.q_tables[i] = self.create_Q_Table(i+2)
                else: # If there's a path, then it loads the content
                    with open(paths[i], "rb") as f:
                        self.q_tables[i] = pickle.load(f)
        
        else:
            print("##Wrong number of paths for loading all of the Agent Q Tables##")

    def create_Q_Table(self, number_of_pawns):
        print("Creating Q Table: ", number_of_pawns)
        new_q_table = {}

        # If there are 2 pawns on the table then the agent will always have
        # at least two options each time he rolls the dice, the extra one 
        # would be if he gets 6, time when he can decide wether to take out
        # a pawn or move one that is already on the table

        # The same logic goes for the rest possibilities

        if number_of_pawns == 2:
            for p1 in tqdm(range(0, 64)):
                for p2 in range(0, 64):
                    new_q_table[(p1, p2)] = [0]*(number_of_pawns + 1)

        if number_of_pawns == 3:
            for p1 in tqdm(range(0, 64)):
                for p2 in range(0, 64):
                    for p3 in range(0, 64):
                        new_q_table[(p1, p2, p3)] = [0]*(number_of_pawns + 1)

        if number_of_pawns == 4:
            for p1 in tqdm(range(0, 64)):
                for p2 in range(0, 64):
                    for p3 in range(0, 64):
                        for p4 in range(0, 64):
                            new_q_table[(p1, p2, p3, p4)] = [0]*(number_of_pawns + 1)

        return new_q_table
        

    def save_Q_Tables(self):
        for i in range(3):
            with open(f"q_table-{i+2}.pickle", "wb") as f:
                pickle.dump(self.q_tables[i], f)
                print("Saved Q Table: ", i)
                # del self.q_table 

    def save_Rewards_Log(self, rewards_of_training):
        with open(f"rewards-{time.time()}.pickle", "wb") as f:
            pickle.dump(rewards_of_training, f)
            print("Saved Rewards")
            # del self.q_table 

    # ------------------------------------------------------------------------------------------------------------------------------
    # DECISION TAKING --------------------------------------------------------------------------------------------------------------

    def get_Action(self, state, number_of_pawns, dice_number_is_6):
        if dice_number_is_6:
            # If dice number is 6 then the agent has the option of choosing to put one pawn on the table
            actions_list = self.q_tables[number_of_pawns - 2][state]
        else:
            # If the dice number isn't 6 then the agent can only choose between moving one of the pawns
            # he already has on the table
            actions_list = self.q_tables[number_of_pawns - 2][state][:number_of_pawns]
        
        action = np.argmax(actions_list)
        print("Decision tooked: ", action)
        return action

    def update_Q_Table(self, number_of_pawns_s, state, action, reward, learning_rate, discount_rate, new_state, number_of_pawns_ns):
        actual_q_value = self.q_tables[number_of_pawns_s - 2][state][action]
        if number_of_pawns_ns > 1:
            next_state_max_value = np.max(self.q_tables[number_of_pawns_ns - 2][new_state])
        else:
            next_state_max_value = 1

        # Equation for calculating the new q value 
        self.q_tables[number_of_pawns_s - 2][state][action] = actual_q_value + learning_rate * (reward + discount_rate * next_state_max_value) - actual_q_value
        print("Q Table value updated")