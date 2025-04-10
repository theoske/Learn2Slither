import argparse
from Play import Play
from Agent import Agent
import os.path
from Train import Train


def main():
    parser = argparse.ArgumentParser(description="Learn2Slither")
    parser.add_argument("--sessions", type=int, help="number of sessions")
    parser.add_argument("--mode", type=str, help="train or play a model")
    parser.add_argument("--modelname", type=str, help="chose an existing model\
                        (npy file) to continue training or display")
    parser.add_argument("--ui", type=str, help="<on/off> decides if want to\
                        display a game of the model")
    parser.add_argument("--rate", type=str, help="<step/human/cpu> decides if\
                        want to train/play model step-by-step or human\
                        readable or computer speed")

    args = parser.parse_args()
    if not (args.modelname and args.sessions and args.mode and args.ui and args.rate):
        print_error()
    rate_map = {"step": 0, "human": 1, "cpu": 2}
    rate = rate_map.get(args.rate, 0)
    if os.path.isfile(args.modelname):
        if args.mode == "train" and args.sessions:
            agent = Agent()
            agent.load_q_table(args.modelname)
            if args.sessions > 0:
                if args.ui == "on":
                    t = Train(num_episodes=args.sessions,
                              qtable_filename=args.modelname,
                              agent=agent, rate=rate, is_ui_on=True)
                else:
                    t = Train(num_episodes=args.sessions,
                              qtable_filename=args.modelname,
                              agent=agent, rate=rate, is_ui_on=False)
                t.train()
        elif args.mode == "play" and args.sessions and args.sessions > 0:
            len_list = []
            duration_list = []
            for i in range(args.sessions):
                g = Play(rate=2, is_ui_on=False, multi_sess=True)
                max_len, duration = g.display_gameplay_term(args.modelname)
                len_list.append(max_len)
                duration_list.append(duration)
                print(i)
            avg_len = sum(len_list) / len(len_list)
            avg_duration = sum(duration_list) / len(duration_list)
            len_list.sort()
            print(f"Average length: {avg_len}   Average duration {avg_duration}\
                     Max length: {max(len_list)}   Median: {len_list[args.sessions//2]}")
        elif args.mode == "play":
            if args.ui == "on":
                g = Play(rate=rate, is_ui_on=True)
            else:
                g = Play(rate=rate, is_ui_on=False)
            g.display_gameplay_ui(args.modelname)
        else:
            print_error()
    elif os.path.isfile(args.modelname) is False and args.sessions:
        if args.mode == "train":
            agent = Agent()
            if args.rate is None:
                rate = 0
            if args.sessions > 0:
                if (args.ui == "on"):
                    print("good")
                    t = Train(num_episodes=args.sessions,
                              qtable_filename=args.modelname,
                              agent=agent, rate=rate, is_ui_on=True)
                else:
                    t = Train(num_episodes=args.sessions,
                              qtable_filename=args.modelname,
                              agent=agent, rate=rate, is_ui_on=False)
                t.train()
        elif args.mode == "play":
            print("Error : Need an existing model to make it play")
            exit(0)
    else:
        print_error()


def print_error():
    print("Usage: python3 snake.py --modelname <filename.npy> \
          --mode <train/play> --sessions <int> --ui <on/off>")
    exit(1)


if __name__ == "__main__":
    main()
