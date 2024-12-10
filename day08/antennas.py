#!/usr/bin/env python3
from dataclasses import dataclass
from itertools import combinations


@dataclass
class Antenna:
    x: int
    y: int
    freq: bytes


def antinode(a0: Antenna, a1: Antenna, xlimit: int, ylimit: int):
    res = []
    if 2 * a0.x - a1.x >= 0 and 2 * a0.x - a1.x < xlimit and 2 * a0.y - a1.y >= 0 and 2 * a0.y - a1.y < ylimit:
        res.append((2 * a0.x - a1.x, 2 * a0.y - a1.y))
    if 2 * a1.x - a0.x >= 0 and 2 * a1.x - a0.x < xlimit and 2 * a1.y - a0.y >= 0 and 2 * a1.y - a0.y < ylimit:
        res.append((2 * a1.x - a0.x, 2 * a1.y - a0.y))
    return set(res)

def harmonics(a0: Antenna, a1: Antenna, xlimit: int, ylimit: int):
    res = []
    px = a0.x
    py = a0.y
    while px >= 0 and px < xlimit and py >= 0 and py < xlimit:
        res.append((px,py))
        px += a0.x-a1.x
        py += a0.y-a1.y
    px = a1.x
    py = a1.y
    while px >= 0 and px < xlimit and py >= 0 and py < xlimit:
        res.append((px,py))
        px += a1.x-a0.x
        py += a1.y-a0.y
    return set(res)


def main():
    with open("input", "r") as reader:
        citymap = []
        y = 0
        line = reader.readline()
        while line != "":  # The EOF char is an empty string
            line = line.rstrip()
            xlimit = len(line)
            for x, f in enumerate(line):
                if f != ".":
                    citymap.append(Antenna(x, y, f))
            line = reader.readline()
            y += 1
    ylimit = y
    frequencies = set(a.freq for a in citymap)
    an = set()
    ham = set()
    for f in frequencies:
        nodes = [a for a in citymap if a.freq == f]
        for resonance in combinations(nodes, 2):
            an |= antinode(resonance[0], resonance[1], xlimit, ylimit)
            ham |= harmonics(resonance[0], resonance[1], xlimit, ylimit)
    print(f"p1: {len(an)}")
    print(f"p2: {len(ham)}")


if __name__ == "__main__":
    main()
