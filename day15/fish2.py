#!/usr/bin/env python3
import argparse
from enum import Enum

DEBUG = False
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

    def get(self, coord: tuple) -> bytes:
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

    @property
    def robot(self):
        robot_position = None
        for coord, cell in self.map.items():
            if cell == "@":
                if robot_position is None:
                    robot_position = coord
                else:
                    raise RuntimeError(MSG_LOST_ROBOT)
        if robot_position is None:
            raise RuntimeError(MSG_LOST_ROBOT)
        return robot_position

    def push(self, coord: tuple, direction: Direction) -> list:
        brackets = {"[": "]", "]": "["}
        content = self.get(coord)
        next_step = self.get(shift(coord, direction))
        if content == "#":
            print(f"DUMP: {coord} {direction}")
            self.print()
            raise RuntimeError(MSG_HIT_WALL)
        elif content in brackets.keys() and direction in [Direction.UP, Direction.DOWN]:
            bracket_couple = [coord, self.complement(coord)]
            next_step = self.get(shift(coord, direction))
            assert all(self.get(shift(c, direction)) == "." for c in bracket_couple)
            for c in bracket_couple:
                self.put(c, ".")
            self.put(shift(coord, direction), content)
            self.put(self.complement(shift(coord, direction)), brackets[content])
            return bracket_couple
        elif content in ["@", "O"] + list(brackets.keys()):
            assert next_step == "."
            self.put(shift(coord, direction), content)
            self.put(coord, ".")
            return [coord]
        else:
            return []

    def complement(self, coord: tuple) -> tuple:
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
        for coord, cell in self.map.items():
            if cell == ("O", "[")[self.inflated]:
                r += coord[0] + 100 * coord[1]
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


def shift(coord: tuple, direction: Direction) -> tuple:
    delta = {Direction.LEFT: (-1, 0), Direction.UP: (0, -1), Direction.DOWN: (0, 1), Direction.RIGHT: (1, 0)}
    return tuple(map(sum, zip(coord, delta[direction])))


def boxchain(maze: Maze, direction: Direction) -> list:
    stack = []
    check = {maze.robot}
    while True:
        onwards = {c: maze.get(shift(c, direction)) for c in check if c not in stack}
        if any(content == "#" for content in onwards.values()):
            stack = []
            break
        elif any(content == "@" for content in onwards.values()):
            raise RuntimeError(MSG_WRONG_STEP)
        elif any(content in ["[", "]", "O"] for content in onwards.values()):
            sext = [q for q in check if maze.get(shift(q, direction)) in ["[", "]", "O"]]
            if direction == Direction.LEFT:
                sdict = {q[0]: q for q in sext}
                sext = [sdict[q] for q in sorted(sdict.keys(), reverse=True)]
            elif direction == Direction.RIGHT:
                sdict = {q[0]: q for q in sext}
                sext = [sdict[q] for q in sorted(sdict.keys())]
            if direction == Direction.DOWN:
                for q in onwards.keys():
                    if (q[0], q[1] - 1) in stack and q not in stack:
                        stack.append(q)
            if direction == Direction.UP:
                for q in onwards.keys():
                    if (q[0], q[1] + 1) in stack and q not in stack:
                        stack.append(q)
            stack.extend([q for q in sext if q not in stack])
            check = {shift(q, direction) for q in sext} | {maze.complement(shift(q, direction)) for q in sext}
        elif all(content == "." for content in onwards.values()):
            sext = [q for q in check if q not in stack]
            if direction == Direction.LEFT:
                sdict = {q[0]: q for q in sext}
                sext = [sdict[q] for q in sorted(sdict.keys(), reverse=True)]
            elif direction == Direction.RIGHT:
                sdict = {q[0]: q for q in sext}
                sext = [sdict[q] for q in sorted(sdict.keys())]
            stack.extend([q for q in sext if q not in stack])
            break
        else:
            stack = []
            break
    stack.reverse()
    return stack


def main():
    global DEBUG
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Debug ouput", action="store_true")
    parser.add_argument("-p", "--part", type=int, help="part to solve (1 or 2)", default=1)
    parser.add_argument("filename")
    args = parser.parse_args()
    if args.debug:
        DEBUG = True
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

        if DEBUG:
            print("Original")
            maze.print()
        if args.part == 2:
            maze.inflate()
            if DEBUG:
                print("Inflated")
                maze.print()
        for idx, direction in enumerate(moves):
            if DEBUG:
                print("STEP: {} ROBOT: {} DIRECTION: {}".format(idx, maze.robot, direction.name))
            blocks = boxchain(maze, direction)
            if DEBUG:
                if len(blocks):
                    print(f"MOVES STACK: {blocks}")
                else:
                    print("NOT MOVING")
            touched = []
            for coord in blocks:
                if coord not in touched:
                    touched.extend(maze.push(coord, direction))

            if DEBUG:
                maze.print()
        print(maze.gpsum)


if __name__ == "__main__":
    main()
