import sys
import argparse
from game.HelloGame import HelloGame

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke-test", action="store_true", help="Run for a few frames and exit")
    args = parser.parse_args()

    game = HelloGame(smoke_test=args.smoke_test)
    game.Run()

if __name__ == "__main__":
    main()
