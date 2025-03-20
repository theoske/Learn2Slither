import argparse
from Game import Game
import os.path

"""
    Entrainement avec nombre de session et nom du fichier qtable.
    Faire jouer partie a partir de fichier qtable avec ui et sans.
    -> quand sans indiquer le nombre de session jouer et la taille max et le nombre max de coup joués
    continuer entrainement a partir d'un fichier qtabke deja existant.

    parametres : mode (train/play)    session_nb    qtable_file_name    --ui (on/off)
"""
def main():
    parser = argparse.ArgumentParser(description="Example script with arguments.")
    parser.add_argument("--sessions", type=int, help="number of sessions")
    parser.add_argument("--mode", type=str, help="train or play a model")
    parser.add_argument("--modelname", type=str, help="chose an existing model (npy file) to continue training or display")
    parser.add_argument("--ui", type=str, help="<on/off> decides if want to display a game of the model")
    parser.add_argument("--step", type=str, help="<on/off> decides if want to train/play model step-by-step")

    args = parser.parse_args()
    print(f"Number of episodes : {args.sessions}")
    
    #verifier quel si le model existe deja. si oui l'utiliser en fonction du mode (train/display)
    if args.modelname is None or args.modelname.endswith(".npy") is False or args.mode is None:
        print("Usage: python3 snake.py --modelname <filename.npy> --mode <train/play> --sessions <int> --ui <on/off>")
        exit(0)
    elif os.path.isfile(args.modelname):
        if args.mode == "train":
            pass# continue training
        elif args.mode == "play":
            pass#make model play
        else:
            print("Usage: python3 snake.py --modelname <filename.npy> --mode <train/play> --sessions <int> --ui <on/off>")

if __name__ == "__main__":
    main()

def show_gameplay(qtable_filename):
    print("aa")
    g = Game()
    g.display_gameplay(qtable_filename)

#show_gameplay("models/snake100.npy")
