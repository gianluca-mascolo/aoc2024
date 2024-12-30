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

    def push(self, coord: tuple, direction: Direction):
        MATCH = {"[": "]", "]": "["}
        content = self.get(coord)
        if content == "#":
            print(f"DUMP: {coord} {direction}")
            self.print()
            raise RuntimeError(MSG_HIT_WALL)
        next_step = self.get(shift(coord, direction))
        if next_step != "." and content in ["@", "O"]:
            print(f"DUMP: {coord} {direction}")
            self.print()
            raise RuntimeError("Dot not")
        if content in ["@", "O"]:
            self.put(shift(coord, direction), content)
            self.put(coord, ".")
            return [coord]
        if content in MATCH.keys() and direction in [Direction.UP,Direction.DOWN]:
            mv = [coord, self.companion(coord)]
            next_step = self.get(shift(coord, direction))
            assert next_step == '.'
            for c in mv:
                self.put(c, ".")
            self.put(shift(coord, direction), content)
            self.put(self.companion(shift(coord, direction)), MATCH[content])
            return mv
        if content in MATCH.keys() and direction in [Direction.LEFT,Direction.RIGHT]:
            next_step = self.get(shift(coord, direction))
            assert next_step == '.'
            self.put(shift(coord, direction), content)
            self.put(coord, ".")
            return [coord]




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
        for coord, cell in self.map.items():
            if cell == ('O','[')[self.inflated]:
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
        return True

def shift(coord: tuple, direction: Direction):
    delta = {Direction.LEFT: (-1, 0), Direction.UP: (0, -1), Direction.DOWN: (0, 1), Direction.RIGHT: (1, 0)}
    return tuple(map(sum, zip(coord, delta[direction])))

def move(maze: Maze, coord: tuple, direction: Direction):
    current = maze.get(coord)
    next_step = maze.get(shift(coord, direction))
    if DEBUG:
        print(
            "coord: {} dir: {} cur: {} next {} ccord: {} comp {} sum {}".format(
                coord, direction.name, current, next_step, maze.companion(coord), maze.get(maze.companion(coord)), maze.gpsum
            )
        )
    has_bracket = True
    stack = []
    check = {coord}
    loopstack = 0
    can_move = False
    while has_bracket and current == "@":
        if DEBUG:
            print(f"ls: {loopstack} s: {stack} c: {check}")
        ns = {c: maze.get(shift(c, direction)) for c in check if c not in stack}
        if DEBUG:
            print("ns",ns)
        if any(n in "#" for n in ns.values()):
            if DEBUG:
                print(f"found a wall at {[k for k,v in ns.items() if v=='#']}")
            has_bracket = False
        elif any(n in ['[',']','O'] for n in ns.values()):
            has_bracket = True
            sext = [q for q in check if maze.get(shift(q, direction)) in ['[',']','O']]
            if direction == Direction.LEFT:
                sdict = {q[0]: q for q in sext}
                sext = [ sdict[q] for q in sorted(sdict.keys(),reverse=True) ]
            elif direction == Direction.RIGHT:
                sdict = {q[0]: q for q in sext}
                sext = [ sdict[q] for q in sorted(sdict.keys()) ]
            if direction == Direction.DOWN:
                for q in ns.keys():
                    if (q[0],q[1]-1) in stack and q not in stack:
                        stack.append(q)
            if direction == Direction.UP:
                for q in ns.keys():
                    if (q[0],q[1]+1) in stack and q not in stack:
                        stack.append(q)
            stack.extend([q for q in sext if q not in stack])
            check = {shift(q, direction) for q in sext} | {maze.companion(shift(q, direction)) for q in sext}
        elif all(n == "." for n in ns.values()):
            has_bracket = False
            can_move = True
            sext = [q for q in check if q not in stack]
            if direction == Direction.LEFT:
                sdict = {q[0]: q for q in sext}
                sext = [ sdict[q] for q in sorted(sdict.keys(),reverse=True) ]
            elif direction == Direction.RIGHT:
                sdict = {q[0]: q for q in sext}
                sext = [ sdict[q] for q in sorted(sdict.keys()) ]
            stack.extend([q for q in sext if q not in stack])
        else:
            has_bracket = False
            stack.extend([q for q in check if q not in stack])
        loopstack += 1
    if current == "@" and DEBUG:
        print("<stack>")
        print(can_move, stack)
        print("</stack>")
    stack.reverse()
    if can_move:
        return stack
    else:
        return []

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

        if args.part == 2:
            if DEBUG:
                print("Original")
                maze.print()
            maze.inflate()
            if DEBUG:
                print("Inflated")
                maze.print()

        for idx, direction in enumerate(moves):
            if DEBUG:
                print(idx, maze.robot, direction.name)
            m = move(maze, maze.robot, direction)
            p = []
            for c in m:
                if DEBUG:
                    print(f"PUSHING {c} {direction.name}")
                if c not in p:
                    rr = maze.push(c,direction)
                    p.extend(rr)

            if DEBUG:
                maze.print()
        print(maze.gpsum)

if __name__ == "__main__":
    main()
