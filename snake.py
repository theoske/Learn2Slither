import argparse
from Play import Play
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
    
    rate_map = {"step": 0, "human": 1, "cpu": 2}
    rate = rate_map.get(args.rate, 0)
    if os.path.isfile(args.modelname): #filename exist
        if args.mode == "train": #continue training utiliser load_qtable
            agent = Agent()
            agent.load_q_table(args.modelname)
            if args.sessions > 0:
                if args.ui == "on":
                    t = Train(num_episodes=args.sessions, agent= agent, is_ui_on=True)
                else:
                    t = Train(num_episodes=args.sessions, agent= agent, is_ui_on=False)
                t.train()
        elif args.mode == "play": #make model play without training it
            if args.ui == "on":
                g = Play(rate=rate, is_ui_on=True)
                g.display_gameplay_ui(args.modelname)
            else:
                g = Play(rate=rate, is_ui_on=False)
                g.display_gameplay_term(args.modelname)
        else:
            print_error()
    elif os.path.isfile(args.modelname) is False: #filename doesnt exist
        if args.mode == "train": #create and train new model
            agent = Agent()
            if args.rate is None:
                rate = 0
            if args.sessions > 0:
                if (args.ui == "on"):
                    print("good")
                    t = Train(num_episodes=args.sessions, qtable_filename=args.modelname, agent= agent, rate= rate, is_ui_on= True)
                else:
                    t = Train(num_episodes=args.sessions, qtable_filename=args.modelname, agent= agent, rate= rate, is_ui_on= False)
                t.train()
        elif args.mode == "play":
            print("Error : Need an existing model to make it play")
            exit(0)
    else:
        print_error()
                

def print_error():
    print("Usage: python3 snake.py --modelname <filename.npy> --mode <train/play> --sessions <int> --ui <on/off>")
    exit(1)

if __name__ == "__main__":
    main()

"""
python3 snake.py --ui on  --modelname testtt.npy --mode train --sessions 100 --rate step
python3 snake.py --ui off  --modelname testtt.npy --mode train --sessions 100 --rate step
python3 snake.py --ui on  --modelname models/snake1000.npy --mode play --rate step
python3 snake.py --ui off  --modelname models/snake1000.npy --mode play --rate step
"""