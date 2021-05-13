from models import Ludo_Game_Model
from models import Q_Learning_Smart_Agent_Model

from controllers import Ludo_Game_Controller as lgc
import numpy as np
import matplotlib.pyplot as plt
import PIL

# Identifiers for actions
PUT_PAWN_ON_TABLE = 1
MOVE_PAWN = 2
PUT_PAWN_ON_TABLE_ACTION = (-1, None, PUT_PAWN_ON_TABLE)

# Number of episodes and steps for the training
NUMBER_OF_EPISODES = 1000
MAX_NUMBER_OF_STEPS = 100

# Values for calculating the optimal q* in the Q-Table
LEARNING_RATE = 0.1
DISCOUNT_RATE = 0.99

MAX_EXPLORATION_RATE = 1
MIN_EXPLORATION_RATE = 0.01
EXPLORATION_DECAY = 0.001

# Rewards given
PUT_PAWN_ON_TABLE_REWARD = 1
EAT_PAWN_REWARD = 2
PUT_PAWN_AT_HOME_REWARD = 2

#q_tables = ["q_table-2.pickle", "q_table-3.pickle", "q_table-4.pickle"]
q_tables = [None, None, None]

class Ludo_Engine():
    def __init__(self):
        self.ludo_game = Ludo_Game_Model.Ludo_Game()
        self.smart_agent = Q_Learning_Smart_Agent_Model.QL_Smart_Agent(q_tables)
        self.exploration_rate = 1
        self.done = False

    def play_console(self, number_of_players, model_players):
        self.ludo_game.initialize(number_of_players)
        self.ludo_game.set_To_Start()
        self.done = False

        while self.done is not True:
            for i in range(number_of_players):
                print(f"Turno del jugador {i+1} ------------------------")

                if i > (model_players - 1):
                    lgc.get_Player_Decision(i + 1, "please enter 1 to roll the dice: ", ["1"])

                self.ludo_game.roll_Dice()
                input()

                possible_moves = self.ludo_game.get_Possible_Moves(i)

                if len(possible_moves) > 0:
                    if i > (model_players - 1):
                        lgc.display_Pawn_Options(possible_moves)
                        decision = lgc.get_Player_Decision(i + 1, "please choose an action: ", [str(x) for x in range(len(possible_moves))])
                    else:
                        exploration_rate_th = np.random.uniform(0,1)

                        if len(possible_moves) > 2 :
                            possible_moves, possible_moves_substracted, number_of_pawn_moves = lgc.get_Possible_Moves_Analized(possible_moves, self.ludo_game.can_Put_Pawn_In_Table(i))
                            state = lgc.adapt_State(self.ludo_game, number_of_pawn_moves, i, possible_moves_substracted)

                            if (number_of_pawn_moves > 1) & (exploration_rate_th > self.exploration_rate):
                                decision = self.smart_agent.get_Action(state, number_of_pawn_moves, self.ludo_game.can_Put_Pawn_In_Table(i))
                            else:
                                decision = np.random.randint(0, len(possible_moves))
                        else:
                            decision = np.random.randint(0, len(possible_moves))

                    p_id, _, act = possible_moves[decision]

                    if act == PUT_PAWN_ON_TABLE:
                        self.ludo_game.put_Pawn_In_Table(i)
                    else:
                        self.ludo_game.advance_In_Table(i, p_id)

                else:
                    print("\n0 possible moves\n")

                lgc.display_Table_For_User(self.ludo_game.ludo_table, self.ludo_game.last_cells)
                input()


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
                    print(f"\nPlayer turn: {i + 1} index: {i}")
                    possible_moves_substracted = []
                    exploration_rate_th = np.random.uniform(0,1)

                    self.ludo_game.roll_Dice()
                    self.ludo_game.display_Ludo_Table()
                    possible_moves = self.ludo_game.get_Possible_Moves(i)

                    if len(possible_moves) > 2 :
                        possible_moves, possible_moves_substracted, number_of_pawn_moves = lgc.get_Possible_Moves_Analized(possible_moves, self.ludo_game.can_Put_Pawn_In_Table(i))
                        state = lgc.adapt_State(self.ludo_game, number_of_pawn_moves, i, possible_moves_substracted)

                        if (number_of_pawn_moves > 1) & (exploration_rate_th > self.exploration_rate):
                            decision = self.smart_agent.get_Action(state, number_of_pawn_moves, self.ludo_game.can_Put_Pawn_In_Table(i))
                        else:
                            decision = np.random.randint(0, len(possible_moves))

                        p_id, loc, act = possible_moves[decision]

                        if act == PUT_PAWN_ON_TABLE:
                            new_pawn_id = self.ludo_game.put_Pawn_In_Table(i)
                            possible_moves_substracted.append((new_pawn_id, _, _))

                            self.smart_agent.update_Q_Table(number_of_pawn_moves, state, decision, PUT_PAWN_ON_TABLE_REWARD, LEARNING_RATE, 
                                DISCOUNT_RATE, lgc.adapt_State(self.ludo_game, number_of_pawn_moves + 1, i, possible_moves_substracted), number_of_pawn_moves + 1)

                            rewards_of_the_episode += PUT_PAWN_ON_TABLE_REWARD

                        else:
                            consecuence, _ = self.ludo_game.advance_In_Table(i, p_id)

                            if consecuence < 0:
                                reward = PUT_PAWN_AT_HOME_REWARD
                                possible_moves_substracted.remove((p_id, loc, act))
                                self.smart_agent.update_Q_Table(number_of_pawn_moves, state, decision, reward, LEARNING_RATE, DISCOUNT_RATE, 
                                    lgc.adapt_State(self.ludo_game, number_of_pawn_moves - 1, i, possible_moves_substracted), number_of_pawn_moves - 1)
                            else:
                                if consecuence > 0:
                                    reward = EAT_PAWN_REWARD
                                else:
                                    reward = 0

                                self.smart_agent.update_Q_Table(number_of_pawn_moves, state, decision, reward, LEARNING_RATE, DISCOUNT_RATE, 
                                    lgc.adapt_State(self.ludo_game, number_of_pawn_moves, i, possible_moves_substracted), number_of_pawn_moves)
                            
                            rewards_of_the_episode += reward

                    elif len(possible_moves) > 0:
                        decision = np.random.randint(0, len(possible_moves))
                        p_id, _, act = possible_moves[decision]

                        if act == PUT_PAWN_ON_TABLE:
                            new_pawn_id = self.ludo_game.put_Pawn_In_Table(i)
                        else:
                            self.ludo_game.advance_In_Table(i, p_id)

                    if self.ludo_game.game_Done(i):
                        break
                    
                if self.ludo_game.game_Done(i):
                    break

            self.exploration_rate = MIN_EXPLORATION_RATE + (MAX_EXPLORATION_RATE - MIN_EXPLORATION_RATE) * np.exp(-EXPLORATION_DECAY * episode)
            rewards_of_the_training.append(rewards_of_the_episode)

        print("Training finished")
        self.smart_agent.save_Q_Tables()
        self.smart_agent.save_Rewards_Log(rewards_of_the_training)