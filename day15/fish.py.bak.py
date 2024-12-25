#!/usr/bin/env python3
import argparse
from enum import Enum

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

    def push(self, coord: tuple, direction: bytes):
        content = self.get(coord)
        if content in ["@", "O"]:
            self.put(shift(coord, direction), content)
            self.put(coord, ".")
        elif content == "[" and direction == "<":
            self.put(shift(coord, direction), content)
            self.put(coord, "]")
        elif content == "]" and direction == "<":
            self.put(shift(coord, direction), content)
            self.put(coord, ".")
        elif content == "[" and direction == ">":
            self.put(shift(coord, direction), content)
            self.put(coord, ".")
        elif content == "]" and direction == ">":
            self.put(shift(coord, direction), content)
            self.put(coord, "[")
        elif content in ["[", "]"] and direction in ["^", "v"]:
            self.put(shift(coord, direction), content)
            self.put(coord, ".")
        elif content == "#":
            raise RuntimeError(MSG_HIT_WALL)
        return True

    def companion(self, coord: tuple):
        c = self.get(coord)
        if c == "[":
            return shift(coord, ">")
        elif c == "]":
            return shift(coord, "<")
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
            self.xlimit = 2 * x + 1
            self.inflated = True
        return True


def move(maze: Maze, coord: tuple, direction: bytes):
    current = maze.get(coord)
    next_step = maze.get(shift(coord, direction))
    if next_step == "." and current not in ["[", "]"]:
        maze.push(coord, direction)
        return True
    elif next_step == "." and current in ["[", "]"] and direction in ["^", "v"]:
        closing_position = maze.companion(coord)
        if maze.get(shift(closing_position, direction)) == ".":
            maze.push(coord, direction)
            maze.push(closing_position, direction)
            return True
    elif next_step == "." and current == "[" and direction == "<":
        closing_position = maze.companion(coord)
        maze.push(coord, direction)
        maze.push(closing_position, direction)
        return True
    elif next_step == "." and current == "]" and direction == ">":
        closing_position = maze.companion(coord)
        maze.push(coord, direction)
        maze.push(closing_position, direction)
        return True
    elif next_step in ["[", "]"]:
        if direction == "<" and next_step == "]":
            if move(maze, shift(coord, direction), direction):
                maze.push(coord, direction)
                return True
        if direction == "<" and next_step == "[":
            beyond = shift(shift(coord, direction), direction)
            if maze.get(beyond) == ".":
                maze.push(shift(coord, direction), direction)
                return True
            elif maze.get(beyond) == "]":
                if move(maze, beyond, direction):
                    maze.push(shift(coord, direction), direction)
                    return True
        elif direction == ">" and next_step == "[":
            if move(maze, shift(coord, direction), direction):
                maze.push(coord, direction)
                return True
        elif direction == ">" and next_step == "]":
            beyond = shift(shift(coord, direction), direction)
            if maze.get(beyond) == ".":
                maze.push(shift(coord, direction), direction)
                return True
            elif maze.get(beyond) == "[":
                if move(maze, beyond, direction):
                    maze.push(shift(coord, direction), direction)
                    return True
        elif direction == "^":
            closing_position = maze.companion(coord)
            brackets_position = [shift(coord, direction), closing_position]
            if DEBUG:
                print(f"BRACKETS: {brackets_position}")
                print([maze.get(shift(bracket, direction)) == "." for bracket in brackets_position])
                print([maze.get(shift(bracket, direction)) in MATCH.keys() for bracket in brackets_position])
            if all([maze.get(shift(bracket, direction)) == "." for bracket in brackets_position]):
                for bracket in brackets_position:
                    maze.push(bracket, direction)
                return True
            if all([maze.get(shift(bracket, direction)) in MATCH.keys() for bracket in brackets_position]):
                attempt_move = [move(maze, shift(bracket, direction), direction) for bracket in brackets_position]
                if all(attempt_move):
                    for bracket in brackets_position:
                        maze.push(bracket, direction)
                    return True
                else:
                    for idx, attempt in enumerate(attempt_move):
                        if attempt:
                            bracket = brackets_position[idx]
                            move(maze=maze, coord=shift(shift(bracket, direction), direction), direction="v")
                    return False
            return False
        elif direction == "v":
            return False

        return False
    elif next_step == "O":
        if move(maze, shift(coord, direction), direction):
            maze.push(coord, direction)
            return True
    elif next_step == "@":
        raise RuntimeError(MSG_WRONG_STEP)
    return False


def shift(coord: tuple, direction: bytes):
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
                    print(idx, maze.robot, direction)
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
                    print(idx, maze.robot, direction)
                move(maze, maze.robot, direction)
                if DEBUG:
                    maze.print()


if __name__ == "__main__":
    main()