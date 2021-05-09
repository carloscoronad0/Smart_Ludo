import numpy as np
from tqdm import tqdm
import pickle
import time

class QL_Smart_Agent:
    def __init__(self, stored_q_table_4, stored_q_table_3, stored_q_table_2):
        self.q_tables = [stored_q_table_2, stored_q_table_3, stored_q_table_4]

    def get_Action(self, state, number_of_pawns):
        actions_list = self.q_tables[number_of_pawns][state]
        action = np.argmax(actions_list)

        return action

    def update_Q_Table(self, number_of_pawns, state, action, reward, learning_rate, discount_rate, new_state):
        actual_q_value = self.q_tables[number_of_pawns][state][action]
        next_state_max_value = np.max(self.q_tables[number_of_pawns][new_state])

        self.q_tables[number_of_pawns][state]][action] = actual_q_value + learning_rate * (reward + discount_rate * next_state_max_value) - actual_q_value)
        print("Q Table value updated")

    def create_Q_Table(self, number_of_pawns):
        print("Creating Q Table: ", number_of_pawns)
        new_q_table = {}

        if number_of_pawns == 2:
            for p1 in tqdm(range(0, 64)):
                for p2 in range(0, 64):
                    new_q_table[(p1, p2)] = [0]*number_of_pawns

        if number_of_pawns == 3:
            for p1 in tqdm(range(0, 64)):
                for p2 in range(0, 64):
                    for p3 in range(0, 64):
                        new_q_table[(p1, p2, p3)] = [0]*number_of_pawns

        if number_of_pawns == 4:
            for p1 in tqdm(range(0, 64)):
                for p2 in range(0, 64):
                    for p3 in range(0, 64):
                        for p4 in range(0, 64):
                            new_q_table[(p1, p2, p3, p4)] = [0]*number_of_pawns

        return new_q_table
        
    def load_Q_Tables(self, paths):
        if len(paths) == len(self.q_tables):
            for i in range(len(paths)):
            if paths[i] is None:
                self.q_tables[i] = self.create_Q_Table(i+2)
            else:
                with open(path, "rb") as f:
                    self.q_tables[i] = pickle.load(f)
        
        else:
            print("Missing paths for loading all of the Agent Q Tables")

    def save_Q_Table(self, number_of_pawns):
        with open(f"q_table-{int(time.time())}.pickle", "wb") as f:
            pickle.dump(self.q_tables[number_of_pawns], f)
            print("Saved Q Table: ", number_of_pawns)
            # del self.q_table 