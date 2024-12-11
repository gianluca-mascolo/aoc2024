#!/usr/bin/env python3
import sys
import argparse

DEBUG = True

def blink(stones: list):
    new_stones = []
    for s in stones:
        if s == 0:
            new_stones.append(1)
        elif len(str(s)) % 2 == 0:
            split = len(str(s)) // 2
            new_stones.append(int(str(s)[:split]))
            new_stones.append(int(str(s)[split:]))
        else:
            new_stones.append(s*2024)
    return new_stones

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--blink", type=int, help="number of blinks", default=25)
    args = parser.parse_args()
    while line := sys.stdin.readline():
        stones = [ int(c) for c in line.rstrip().split(" ") ]
    if DEBUG:
        print(stones)
    for cycle in range(args.blink):
        stones = blink(stones)
        if DEBUG:
            print(stones)
        print(f"cycle {cycle} stones {len(stones)}")


if __name__ == "__main__":
    main()
