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


@dataclass
class Region:
    kind: bytes
    points: set


def mergeregions(regions: list):
    rcopy = [r for r in regions]
    merged = []
    has_merges = False
    merged_list = []
    for position, check in enumerate(rcopy):
        comparison = []
        if position in merged_list:
            print(f"already merged {position}")
            continue
        for other, compare in enumerate(rcopy):
            if other != position:
                comparison.append(bool(check.points & compare.points))
            else:
                comparison.append(False)
        if any(comparison):
            merging_index = comparison.index(True)
            merging_points = rcopy[merging_index].points
            merging_kind = rcopy[merging_index].kind
            merging_region = rcopy[merging_index]
            if check.kind == merging_kind:
                print(f"region {position} against {merging_index}")
                new_region = Region(check.kind, check.points | merging_points)
                print(f"original: {len(check.points)} {check}")
                print(f"merging: {len(merging_points)} {merging_region}")
                print(f"new: {len(new_region.points)} {new_region}")
                merged.append(Region(check.kind, check.points | merging_points))
                merged_list.append(merging_index)
                has_merges = True
            else:
                merged.append(check)
        else:
            merged.append(check)
    print(f"merged regions len: {len(merged)} {has_merges}")
    return merged, has_merges


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
    for point in gardens.keys():
        connections = {point}
        for direction in ["left", "right", "up", "down"]:
            if connected := getattr(gardens[point], direction):
                connections |= {connected}
        neighbors = {c for c in connections}
        for p in connections:
            for direction in ["left", "right", "up", "down"]:
                if connected := getattr(gardens[p], direction):
                    neighbors |= {connected}
        if gardens[point].kind not in [r.kind for r in regions]:
            regions.append(Region(gardens[point].kind, neighbors))
        else:
            glue = False
            for r in regions:
                if r.kind == gardens[point].kind and neighbors & r.points:
                    r.points |= neighbors
                    glue = True
            if not glue:
                regions.append(Region(gardens[point].kind, neighbors))

    print("prima", len(regions))
    overlap = True
    while overlap:
        regions, overlap = mergeregions(regions)
    print("dopo", len(regions))

    print("###")
    result = 0
    for r in regions:
        perimeter = 0
        for p in r.points:
            for direction in ["left", "right", "up", "down"]:
                if getattr(gardens[p], direction) is None:
                    perimeter += 1
        print(r, perimeter, len(r.points), len(r.points) * perimeter)
        result += len(r.points) * perimeter
    print(result)


if __name__ == "__main__":
    main()
