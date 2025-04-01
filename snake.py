import argparse
from Game import Game
from Agent import Agent
import os.path
from Train import Train

"""
    step-by-step avec entrer par défaut en fonction de la commande. Appuyer sur espace pour changer (->human readable -> computer speed).

    Entrainement de nouveau model sans ui.
    Entrainement de nouveau model avec ui.
    Entrainement de model deja existant sans ui.
    Entrainement de model deja existant avec ui.

    Démonstration model sans ui.
    Démonstration model avec ui.
"""
def main():
    parser = argparse.ArgumentParser(description="Example script with arguments.")
    parser.add_argument("--sessions", type=int, help="number of sessions")
    parser.add_argument("--mode", type=str, help="train or play a model")
    parser.add_argument("--modelname", type=str, help="chose an existing model (npy file) to continue training or display")
    parser.add_argument("--ui", type=str, help="<on/off> decides if want to display a game of the model")
    parser.add_argument("--rate", type=str, help="<step/human/cpu> decides if want to train/play model step-by-step or human readable or computer speed")

    args = parser.parse_args()
    print(f"Number of episodes : {args.sessions}")
    
    #verifier quel si le model existe deja. si oui l'utiliser en fonction du mode (train/display)
    if args.modelname is None or args.modelname.endswith(".npy") is False or args.mode is None:#erreur
        print_error()
    elif os.path.isfile(args.modelname):#filename existe
        if args.mode == "train": #continue training utiliser load_qtable
            agent = Agent()
            agent.load_qtable(args.modelname)
            if args.sessions > 0:
                train(num_episodes=args.sessions, agent= agent)
        elif args.mode == "play":# ui on-off
            if args.ui == "on":
                show_gameplay(args.modelname)
            else:
                pass#play no ui
        else:
            print_error()
    elif os.path.isfile(args.modelname) is False:# train basic
        if args.mode == "train":
            agent = Agent()
            rate = int(args.rate)
            if args.rate is None:
                rate = 0
            if args.sessions > 0:
                t = Train(num_episodes=args.sessions, agent= agent, rate= rate)
                t.train()
                

def print_error():
    print("Usage: python3 snake.py --modelname <filename.npy> --mode <train/play> --sessions <int> --ui <on/off>")
    exit(1)

if __name__ == "__main__":
    main()

def show_gameplay(qtable_filename):
    print("aa")
    g = Game()
    g.display_gameplay(qtable_filename)

#show_gameplay("models/snake100.npy")
