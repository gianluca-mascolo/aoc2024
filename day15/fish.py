#!/usr/bin/env python3
import argparse
from enum import Enum
from random import randint

DEBUG = False

MATCH = {"[": "]", "]": "["}

MSG_LOST_ROBOT = "Where are the droids you are looking for?"
MSG_HIT_WALL = "You are not stubborn enough to push a wall"
MSG_WRONG_STEP = "Ouch! You bite your tail"


class Direction(Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


class Maze:
    def __init__(self):
        self.map = {}
        self.xlimit = 0
        self.ylimit = 0
        self.inflated = False

    def put(self, coord: tuple, content: bytes):
        self.map[coord] = content

    def get(self, coord: tuple):
        if coord in self.map:
            return self.map[coord]
        else:
            return "#"

    def print(self):
        for y in range(self.ylimit):
            line = []
            for x in range(self.xlimit):
                line.append(self.get((x, y)))
            print("".join(line))

    def dump(self, filename):
        with open(filename, "w") as f:
            for y in range(self.ylimit):
                for x in range(self.xlimit):
                    f.write(f"({x},{y}): {self.get((x,y))}\n")

    @property
    def robot(self):
        rpos = None
        for coord, cell in self.map.items():
            if cell == "@":
                if rpos is None:
                    rpos = coord
                else:
                    raise RuntimeError(MSG_LOST_ROBOT)
        if rpos is None:
            raise RuntimeError(MSG_LOST_ROBOT)
        return rpos

    def push(self, coord: tuple, direction: Direction):
        content = self.get(coord)
        if content in ["@", "O"]:
            next_step = self.get(shift(coord, direction))
            assert next_step == "."
            self.put(shift(coord, direction), content)
            self.put(coord, ".")
        if content in MATCH.keys():
            next_step = self.get(shift(coord, direction))
            assert next_step in [".", MATCH[content]]
            for c in [coord, self.companion(coord)]:
                self.put(c, ".")
            self.put(shift(coord, direction), content)
            self.put(self.companion(shift(coord, direction)), MATCH[content])
        elif content == "#":
            raise RuntimeError(MSG_HIT_WALL)

    def companion(self, coord: tuple):
        c = self.get(coord)
        if c == "[":
            return shift(coord, Direction.RIGHT)
        elif c == "]":
            return shift(coord, Direction.LEFT)
        else:
            return coord

    @property
    def gpsum(self):
        r = 0
        if not self.inflated:
            for coord, cell in self.map.items():
                if cell == "O":
                    r += coord[0] + 100 * coord[1]
        else:
            for coord, cell in self.map.items():
                if cell == "[":
                    # coord[0]
                    # self.xlimit - coord[0] - 2
                    # coord[1]
                    # self.ylimit - coord[1] - 1
                    # r += min(coord[0],self.xlimit - coord[0] - 2) + 100 * min(coord[1],self.ylimit - coord[1] - 1)
                    r += coord[0] + 100 * coord[1]
        return r

    @property
    def boxes(self):
        r = 0
        if not self.inflated:
            for coord, cell in self.map.items():
                if cell == "O":
                    r += 1
        else:
            for coord, cell in self.map.items():
                if cell == "[":
                    r += 1
        return r

    def inflate(self):
        if not self.inflated:
            newmap = {}
            for coord, cell in self.map.items():
                x = coord[0]
                y = coord[1]
                if cell in ["#", "."]:
                    newmap[(2 * x, y)] = cell
                    newmap[(2 * x + 1, y)] = cell
                elif cell == "O":
                    newmap[(2 * x, y)] = "["
                    newmap[(2 * x + 1, y)] = "]"
                elif cell == "@":
                    newmap[(2 * x, y)] = "@"
                    newmap[(2 * x + 1, y)] = "."
            self.map = {k: v for k, v in newmap.items()}
            self.xlimit = 2 * x + 2
            self.inflated = True
        return True


def move(maze: Maze, coord: tuple, direction: Direction):
    current = maze.get(coord)
    next_step = maze.get(shift(coord, direction))
    if next_step == ".":
        maze.push(coord, direction)
        return True
    elif next_step == "O":
        if move(maze, shift(coord, direction), direction):
            maze.push(coord, direction)
            return True
    elif next_step == "@":
        raise RuntimeError(MSG_WRONG_STEP)
    return False


def move2(maze: Maze, coord: tuple, direction: Direction):
    loopstamp = str(randint(0, 999999)).zfill(6)
    current = maze.get(coord)
    next_step = maze.get(shift(coord, direction))
    if DEBUG:
        print(
            "{} - coord: {} dir: {} cur: {} next {} ccord: {} comp {} sum {} box {}".format(
                loopstamp, coord, direction.name, current, next_step, maze.companion(coord), maze.get(maze.companion(coord)), maze.gpsum, maze.boxes
            )
        )
        has_bracket = True
        stack = []
        check = {coord}
        loopstack = 0
        can_move = False
        while has_bracket and current == "@":
            print(f"ls: {loopstack} s: {stack} c: {check}")
            # print([maze.get(shift(c,direction)) in MATCH.keys() for c in check])
            ns = {c: maze.get(shift(c, direction)) for c in check if c not in stack}
            print(ns)
            if any(n in "#" for n in ns.values()):
                print(f"found a wall at {[k for k,v in ns.items() if v=='#']}")
                has_bracket = False
            elif any(n in MATCH.keys() for n in ns.values()):
                has_bracket = True
                sext = [q for q in check if maze.get(shift(q, direction)) in MATCH.keys()]
                stack.extend([q for q in sext if q not in stack])
                check = {shift(q, direction) for q in sext} | {maze.companion(shift(q, direction)) for q in sext}
            elif all(n == "." for n in ns.values()):
                has_bracket = False
                can_move = True
                stack.extend([q for q in check if q not in stack])
            else:
                has_bracket = False
                stack.extend([q for q in check if q not in stack])
            loopstack += 1
        if current == "@":
            print("<stack>")
            print(can_move, stack)
            print("</stack>")

    if current == "#":
        return False
    if next_step == ".":
        if current == "@":
            maze.push(coord, direction)
            return True
        elif current in MATCH.keys():
            if direction in [Direction.UP, Direction.DOWN]:
                ccoord = shift(maze.companion(coord), direction)
                if maze.get(ccoord) == ".":
                    if DEBUG:
                        print(f"{loopstamp} - MOVING {coord} {current} {direction.name}")
                    maze.push(coord, direction)
                    return True
                elif maze.get(ccoord) in MATCH.keys() and move2(maze, ccoord, direction):
                    maze.push(coord, direction)
                    return True
            elif direction in [Direction.LEFT, Direction.RIGHT]:
                maze.push(coord, direction)
                return True
    elif next_step in MATCH.keys():
        beyond = shift(shift(coord, direction), direction)
        companion = maze.companion(coord)
        prima = maze.get(shift(companion, direction))
        if DEBUG:
            print(f"{loopstamp} - beyond {beyond} {maze.get(beyond)}")
        # if direction in [Direction.UP, Direction.DOWN]:

        if direction in [Direction.UP, Direction.DOWN] and maze.get(shift(companion, direction)) in [".", "[", "]"] and move2(maze, shift(coord, direction), direction):
            read_again = maze.get(shift(companion, direction))
            if DEBUG:
                print(f"{loopstamp} - checking {shift(companion,direction)} prima: {prima} dopo: {read_again}")
            if read_again == ".":
                maze.push(coord, direction)
                return True
            elif move2(maze, shift(companion, direction), direction):
                if DEBUG:
                    print(f"{loopstamp} - PUSHING {coord} {current} {direction.name}")
                maze.push(coord, direction)
                return True
            else:
                # rollback
                if DEBUG:
                    print(f"{loopstamp} ROLLBACK!")
                reverse = {Direction.UP, Direction.DOWN}
                reverse.remove(direction)
                revdir = reverse.pop()
                pos = beyond
                c = maze.get(pos)
                p = c
                stack = []
                while c == p:
                    stack.append(pos)
                    pos = shift(pos, direction)
                    c = maze.get(pos)
                reverse = {Direction.UP, Direction.DOWN}
                reverse.remove(direction)
                revdir = reverse.pop()
                for pos in stack:
                    move2(maze, pos, revdir)
                return False
        elif direction in [Direction.LEFT, Direction.RIGHT] and move2(maze, beyond, direction):
            maze.push(coord, direction)
            return True
    elif next_step == "@":
        raise RuntimeError(MSG_WRONG_STEP)
    return False


def shift(coord: tuple, direction: Direction):
    delta = {Direction.LEFT: (-1, 0), Direction.UP: (0, -1), Direction.DOWN: (0, 1), Direction.RIGHT: (1, 0)}
    return tuple(map(sum, zip(coord, delta[direction])))


def main():
    global DEBUG
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Debug ouput", action="store_true")
    parser.add_argument("-p", "--part", type=int, help="part to solve (1 or 2)", default=1)
    parser.add_argument("filename")
    args = parser.parse_args()
    if args.debug:
        DEBUG = True
    assert args.part in [1, 2]
    with open(args.filename, "r") as reader:
        line = reader.readline()
        loading = "MAZE"
        maze = Maze()
        moves = []
        y = 0
        while line != "":  # The EOF char is an empty string
            line = line.rstrip()
            if line == "":
                loading = "MOVES"
                line = reader.readline()
                continue
            if loading == "MAZE":
                maze.xlimit = len(line)
                for x, cell in enumerate(line):
                    maze.put((x, y), cell)
                y += 1
            elif loading == "MOVES":
                moves.extend(Direction(m) for m in line)
            line = reader.readline()
        maze.ylimit = y

        if args.part == 1:
            for idx, direction in enumerate(moves):
                if DEBUG:
                    print(idx, maze.robot, direction.name)
                move(maze, maze.robot, direction)
                if DEBUG:
                    maze.print()
            print(maze.gpsum)
        else:
            if DEBUG:
                print("Original")
                maze.print()
            maze.inflate()
            if DEBUG:
                print("Inflated")
                maze.print()
            for idx, direction in enumerate(moves):
                if DEBUG:
                    print(f"STEP: {idx} {maze.gpsum}")
                    print(idx, maze.robot, direction.name)
                move2(maze, maze.robot, direction)
                if DEBUG:
                    maze.print()
                if idx >= 14505 and idx <= 14509:
                    maze.dump(f"dump{str(idx).zfill(8)}.txt")
            print(maze.gpsum)

    #     if DEBUG:
    #         print(maze.xlimit)

    # with open("example6", "r") as reader:
    #     line = reader.readline()
    #     loading = "MAZE"
    #     testmaze = Maze()
    #     y = 0
    #     while line != "":  # The EOF char is an empty string
    #         line = line.rstrip()
    #         testmaze.xlimit = len(line)
    #         for x, cell in enumerate(line):
    #             testmaze.put((x, y), cell)
    #         y += 1
    #         line = reader.readline()
    #     testmaze.ylimit = y
    # testmaze.inflated = True
    # print("Ciccio")
    # testmaze.print()
    # print(testmaze.gpsum)


if __name__ == "__main__":
    main()
