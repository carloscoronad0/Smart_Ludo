import Ludo_Game_Engine

game = Ludo_Game_Engine.Ludo_Engine()
#game.train_model(4)
user_decision = ""

while user_decision != "0":
    print("0.- Terminate execution")
    print("1.- Play game against smart agent")
    print("2.- Train smart agent")
    print("Please enter your choice")
    user_decision = input()

    if user_decision == "1":
        game.play_console(4,3)
    elif  user_decision == "2":
        game.train_model(4)

