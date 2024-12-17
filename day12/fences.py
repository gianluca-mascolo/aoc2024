#!/usr/bin/env python3
import argparse
from dataclasses import dataclass
from typing import Optional

DEBUG = False


@dataclass
class Plot:
    kind: bytes
    left: Optional[tuple] = None
    right: Optional[tuple] = None
    up: Optional[tuple] = None
    down: Optional[tuple] = None


def main():
    global DEBUG
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Debug ouput", action="store_true")
    parser.add_argument("filename")
    args = parser.parse_args()
    if args.debug:
        DEBUG = True
    with open(args.filename, "r") as reader:
        gardens = dict()
        y = 0
        line = reader.readline()
        while line != "":  # The EOF char is an empty string
            line = line.rstrip()
            for x, f in enumerate(line):
                gardens[(x, y)] = Plot(f)
                if (x - 1, y) in gardens and gardens[(x - 1, y)].kind == f:
                    if DEBUG:
                        print(f"{y} {f} left")
                    gardens[(x - 1, y)].right = (x, y)
                    gardens[(x, y)].left = (x - 1, y)
                if (x, y - 1) in gardens and gardens[(x, y - 1)].kind == f:
                    if DEBUG:
                        print(f"{y} {f} up")
                    gardens[(x, y - 1)].down = (x, y)
                    gardens[(x, y)].up = (x, y - 1)
            line = reader.readline()
            y += 1
    if DEBUG:
        print(gardens)

    regions = []
    for p in gardens.keys():
        print("check", p, gardens[p])
        for direction in ["left", "right", "up", "down"]:
            if connected := getattr(gardens[p], direction):
                print("conn1", connected)
                for r in regions:
                    if connected in r:
                        r |= {p}

        if any(p in r for r in regions):
            print("trovo")
        else:
            regions.append({p})
            for direction in ["left", "right", "up", "down"]:
                if connected := getattr(gardens[p], direction):
                    print("conn", connected)
                    regions[-1] |= {connected}
    print("XXX")
    for r in regions:
        print(r)


if __name__ == "__main__":
    main()
