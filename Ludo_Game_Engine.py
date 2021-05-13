from models import Ludo_Game_Model
from models import Q_Learning_Smart_Agent_Model
import numpy as np
import matplotlib.pyplot as plt
import PIL

PUT_PAWN_ON_TABLE = 1
MOVE_PAWN = 2

NUMBER_OF_EPISODES = 1000
MAX_NUMBER_OF_STEPS = 100

LEARNING_RATE = 0.1
DISCOUNT_RATE = 0.99

MAX_EXPLORATION_RATE = 1
MIN_EXPLORATION_RATE = 0.01
EXPLORATION_DECAY = 0.001

PUT_PAWN_ON_TABLE_REWARD = 1
EAT_PAWN_REWARD = 2


#q_tables = ["q_table-2.pickle", "q_table-3.pickle", "q_table-4.pickle"]
q_tables = [None, None, None]

class Ludo_Engine():
    def __init__(self):
        self.ludo_game = Ludo_Game_Model.Ludo_Game()
        self.smart_agent = Q_Learning_Smart_Agent_Model.QL_Smart_Agent(q_tables)
        self.exploration_rate = 1
        self.done = False

    def plot_Rewards_On_Games(self, rewards, number_of_games):
        fig, ax = plt.subplots()
        ax.bar(number_of_games, rewards)
        fig.show()

#    def get_Possible_Moves(self, dice_number, player_number):
#        return self.ludo_game.get_Possible_Moves(dice_number, player_number)

    def play_console(self, number_of_players):
        player_desicion = 0

        while self.done is not True:
            for i in range(number_of_players):

                while player_desicion != 1:
                    print(f"Player {i}, please enter '1' to roll the dice")
                    player_desicion = int(input())
                    self.ludo_game.roll_Dice()
                    print(f"Dice number: {self.ludo_game.dice}")

                player_desicion = 0
                possible_moves = self.get_Possible_Moves(self.ludo_game.dice, i)
                display = len(possible_moves)

                print(f"Actions: \n\tPut Pawn on Table: {PUT_PAWN_ON_TABLE} \n\tMove Pawn{MOVE_PAWN}")
                print("Possible moves: \n")
                for i in range(display):
                    p_id, loc, act = possible_moves[i]
                    print(f"{i}.- Pawn {p_id} in location {loc} with possible action {act}\n")

                while player_desicion <= 0 | player_desicion >= display:
                    print(f"Please enter the index of the desicion you choose ")
                    player_desicion = int(input())

    def adapt_State(self, number_of_pawn_moves, player_number, possible_moves):
        print("Moves on adapt: ", possible_moves)
        if number_of_pawn_moves == 1:
            pn1, _, _ = possible_moves[0]
            state = (self.ludo_game.get_Pawn_State(player_number,pn1))

        if number_of_pawn_moves == 2:
            pn1, _, _ = possible_moves[0]
            pn2, _, _ = possible_moves[1]
            state = (self.ludo_game.get_Pawn_State(player_number, pn1), self.ludo_game.get_Pawn_State(player_number, pn2))
                                    
        elif number_of_pawn_moves == 3:
            pn1, _, _ = possible_moves[0]
            pn2, _, _ = possible_moves[1]
            pn3, _, _ = possible_moves[2]
            state = (self.ludo_game.get_Pawn_State(player_number, pn1), self.ludo_game.get_Pawn_State(player_number, pn2), 
                self.ludo_game.get_Pawn_State(player_number, pn3))

        elif number_of_pawn_moves == 4:
            pn1, _, _ = possible_moves[0]
            pn2, _, _ = possible_moves[1]
            pn3, _, _ = possible_moves[2]
            pn4, _, _ = possible_moves[3]
            state = (self.ludo_game.get_Pawn_State(player_number, pn1), self.ludo_game.get_Pawn_State(player_number, pn2), 
                self.ludo_game.get_Pawn_State(player_number, pn3), self.ludo_game.get_Pawn_State(player_number, pn4))

        return state

    def train_model(self, number_of_players):
        rewards_of_the_training = []

        for episode in range(NUMBER_OF_EPISODES):
            self.ludo_game.initialize(number_of_players)
            self.ludo_game.set_To_Start()
            self.done = False
            rewards_of_the_episode = 0
            possible_moves = []

            print("Begining of episode ----------------------------------------------------")
            for step in range(MAX_NUMBER_OF_STEPS):
                for i in range(number_of_players):
                    print(f"\nPlayer turn: {i + 1} index: {i}-----------------------------------------------\n")
                    possible_moves_substracted = []
                    exploration_rate_th = np.random.uniform(0,1)

                    self.ludo_game.roll_Dice()
                    print("Dice: ", self.ludo_game.dice)

                    possible_moves = self.ludo_game.get_Possible_Moves(i)
                    print("Possible moves: ", len(possible_moves))

                    if len(possible_moves) > 2 :
                        possible_moves_substracted = possible_moves.copy()
                    
                        if self.ludo_game.can_Put_Pawn_In_Table(i):
                            number_of_pawn_moves = len(possible_moves) - 1
                            possible_moves_substracted.remove((-1, None, PUT_PAWN_ON_TABLE))
                        else:
                            number_of_pawn_moves = len(possible_moves)

                        state = self.adapt_State(number_of_pawn_moves, i, possible_moves_substracted)

                        if (number_of_pawn_moves > 1) & (exploration_rate_th > self.exploration_rate):
                            decision = self.smart_agent.get_Action(state, number_of_pawn_moves, self.ludo_game.can_Put_Pawn_In_Table(i))

                        else:
                            decision = np.random.randint(0, len(possible_moves))

                        p_id, loc, act = possible_moves[decision]

                        if act == PUT_PAWN_ON_TABLE:
                            new_pawn_id = self.ludo_game.put_Pawn_In_Table(i)
                            possible_moves_substracted.append((new_pawn_id, _, _))

                            print("Put pawn in table")
                            self.smart_agent.update_Q_Table(number_of_pawn_moves, state, decision, PUT_PAWN_ON_TABLE_REWARD, LEARNING_RATE, 
                                DISCOUNT_RATE, self.adapt_State(number_of_pawn_moves + 1, i, possible_moves_substracted), number_of_pawn_moves + 1)

                            rewards_of_the_episode += PUT_PAWN_ON_TABLE_REWARD

                        else:
                            consecuence, consecuence_loc = self.ludo_game.advance_In_Table(i, p_id)
                            print(f"Moving pawn, consecuence {consecuence} loc {consecuence_loc}")

                            if consecuence < 0:
                                reward = EAT_PAWN_REWARD
                                possible_moves_substracted.remove((p_id, loc, act))
                                self.smart_agent.update_Q_Table(number_of_pawn_moves, state, decision, reward, LEARNING_RATE, DISCOUNT_RATE, 
                                    self.adapt_State(number_of_pawn_moves - 1, i, possible_moves_substracted), number_of_pawn_moves - 1)
                            else:
                                if consecuence > 0:
                                    reward = EAT_PAWN_REWARD
                                    self.ludo_game.pawn_Has_Been_Eaten(int(consecuence - 1), consecuence_loc)
                                else:
                                    reward = 0

                                print("Pawns: ", number_of_pawn_moves)
                                print("State: ", state)
                                self.smart_agent.update_Q_Table(number_of_pawn_moves, state, decision, reward, 
                                    LEARNING_RATE, DISCOUNT_RATE, self.adapt_State(number_of_pawn_moves, i, possible_moves_substracted), number_of_pawn_moves)
                            
                            rewards_of_the_episode += reward

                    elif len(possible_moves) > 0:
                        decision = np.random.randint(0, len(possible_moves))
                        p_id, _, act = possible_moves[decision]

                        if act == PUT_PAWN_ON_TABLE:
                            new_pawn_id = self.ludo_game.put_Pawn_In_Table(i)
                        else:
                            self.ludo_game.advance_In_Table(i, p_id)

                    self.done = self.ludo_game.game_Done(i)
                    if self.done:
                        break
                    
                if self.done:
                    break

            self.exploration_rate = MIN_EXPLORATION_RATE + (MAX_EXPLORATION_RATE - MIN_EXPLORATION_RATE) * np.exp(-EXPLORATION_DECAY * episode)
            rewards_of_the_training.append(rewards_of_the_episode)

        print("Training finished")
        self.plot_Rewards_On_Games(rewards_of_the_training, NUMBER_OF_EPISODES)
        self.smart_agent.save_Q_Tables()
        self.smart_agent.save_Rewards_Log(rewards_of_the_training)