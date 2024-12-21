#!/usr/bin/env python3
import argparse
import re

DEBUG = False


def main():
    global DEBUG
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Debug ouput", action="store_true")
    parser.add_argument("-w", "--wide", type=int, help="field width", required=True)
    parser.add_argument("-t", "--tall", type=int, help="field height", required=True)
    parser.add_argument("-s", "--seconds", type=int, help="run for seconds", default=100)
    parser.add_argument("filename")
    args = parser.parse_args()
    wide = args.wide
    run = args.seconds
    tall = args.tall
    if args.debug:
        DEBUG = True
    if DEBUG:
        print(f"wide: {wide}, tall: {tall} run: {run}")
    line_regex = re.compile("^p=([0-9-]+),([0-9-]+)[ ]+v=([0-9-]+),([0-9-]+)$")
    robots = []
    with open(args.filename, "r") as reader:
        line = reader.readline()
        while line != "":  # The EOF char is an empty string
            line = line.rstrip()
            line_array = line_regex.split(line)
            px = int(line_array[1])
            py = int(line_array[2])
            vx = int(line_array[3])
            vy = int(line_array[4])
            if DEBUG:
                print(f"px: {px} py: {py} vx: {vx} vy: {vy}")
            robots.append({"px": px, "py": py, "vx": vx, "vy": vy})
            line = reader.readline()
    if DEBUG:
        print(robots[0])
    for robot in robots:
        nx = (robot["px"] + robot["vx"] * run) % wide
        ny = (robot["py"] + robot["vy"] * run) % tall
        robot["px"] = nx
        robot["py"] = ny
    if DEBUG:
        print(robots[0])

    hw = (wide - 1) // 2
    ht = (tall - 1) // 2
    quadrants = [(hw, 1, ht, 1), (hw, -1, ht, 1), (hw, 1, ht, -1), (hw, -1, ht, -1)]
    result = 1
    for q in quadrants:
        qx = q[0]
        cx = q[1]
        qy = q[2]
        cy = q[3]
        result *= len(list(filter(lambda r: cx * (r["px"] - qx) < 0 and cy * (r["py"] - qy) < 0, robots)))
    print(result)


if __name__ == "__main__":
    main()
