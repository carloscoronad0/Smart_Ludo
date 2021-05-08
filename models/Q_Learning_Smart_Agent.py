import numpy as np
from tqdm import tqdm

class QL_Smart_Agent:
    def __init__(self, stored_q_table):
        self.q_table = stored_q_table

    def get_Action(self, state):
        actions_list = self.q_table[state]
        action = np.argmax(actions_list)

        return action

    def update_Q_Table(self, state, action, reward, learning_rate, discount_rate, new_state):
        actual_q_value = self.q_table[state][action]
        next_state_max_value = np.max(self.q_table[new_state])

        self.q_table[state]][action] = actual_q_value + learning_rate * (reward + discount_rate * next_state_max_value) - actual_q_value)

    def create_Q_Table(self):
        new_q_table = {}

        for p1 in tqdm(range(-1, 64)):
            for p2 in range(-1, 64):
                for p3 in range(-1, 64):
                    for p4 in range(-1, 64):
                        new_q_table[(p1, p2, p3, p4)] = [np.zeros(4)]

        return new_q_table

    