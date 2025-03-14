import argparse

def main():
    parser = argparse.ArgumentParser(description="Example script with arguments.")
    parser.add_argument("--sessions", type=int, help="number of sessions")
    parser.add_argument("--mode", type=str, help="train or display a model")
    parser.add_argument("--modelname", type=str, help="chose an existing model (npy file) to continue training or display")

    args = parser.parse_args()
    print(f"Number of episodes : {args.sessions}")
    
    if args.sessions:
        print(f"{args.mode}")

if __name__ == "__main__":
    main()