#!/usr/bin/env python3
import argparse

DEBUG = False

DIRECTIONS = {"<": (-1, 0), "^": (0, -1), "v": (0, 1), ">": (1, 0)}


def move(cell: tuple, maze: list, direction: bytes):
    xlimit = len(maze[0])
    ylimit = len(maze)
    dx = DIRECTIONS[direction][0]
    dy = DIRECTIONS[direction][1]
    x = cell[0]
    y = cell[1]
    if x + dx < 0 or x + dx >= xlimit or y + dy < 0 or y + dy >= ylimit:
        return cell
    elif maze[y + dy][x + dx] == "#":
        return cell
    elif maze[y + dy][x + dx] == ".":
        if maze[y][x] == "[" and maze[y + dy][x + dx + 1] in [".", "["]:
            maze[y][x] = '.'
            maze[y][x+1] = '.'
            maze[y + dy][x + dx] = '['
            maze[y + dy][x + dx + 1] = ']'
        elif maze[y][x] == "]" and maze[y + dy][x + dx - 1] in [".", "]"]:
            maze[y][x] = '.'
            maze[y][x-1] = '.'
            maze[y + dy][x + dx] = ']'
            maze[y + dy][x + dx - 1] = '['
        else:
            maze[y][x], maze[y + dy][x + dx] = maze[y + dy][x + dx], maze[y][x]
        return (x + dx, y + dy)
    elif maze[y + dy][x + dx] == "O":
        newpos = move(cell=(x + dx, y + dy), maze=maze, direction=direction)
        if newpos != (x + dx, y + dy):
            maze[y][x], maze[y + dy][x + dx] = maze[y + dy][x + dx], maze[y][x]
            return (x + dx, y + dy)
        else:
            return cell
    elif maze[y + dy][x + dx] == "[" or maze[y + dy][x + dx] == "]":
        print(f"JUMP {maze[y + dy][x + dx]} {x} {y} {dx} {dy}")
        newpos = move(cell=(x + 2 * dx, y + dy), maze=maze, direction=direction)
        print(f"NP: {newpos} cell: {cell} delta: {DIRECTIONS[direction]}")
        xshift = x+2*dx-newpos[0]
        yshift = y+2*dy-newpos[1]
        if xshift or yshift:
            print(f"SHIFT: {xshift} {yshift}")
            if maze[y+dy][x+dx] == '[':
                current = maze[y][x]
                print(f"A {current}")
            elif maze[y+dy][x+dx] == ']':
                current = maze[y][x]
                print(f"B {current}")

            elif maze[y+dy][x+dx] == '.':
                print("NORMAL")
                if maze[y][x] == "[":
                    maze[y][x] = '.'
                    maze[y][x+1] = '.'
                    maze[y + dy][x + dx] = '['
                    maze[y + dy][x + dx + 1] = ']'
                elif maze[y][x] == "[":
                    maze[y][x] = '.'
                    maze[y][x-1] = '.'
                    maze[y + dy][x + dx] = ']'
                    maze[y + dy][x + dx - 1] = '['
                else:
                    maze[y][x], maze[y + dy][x + dx] = maze[y + dy][x + dx], maze[y][x]

            return(x+ dx, y+dy)
        else:
            return cell
    else:
        print("unknown")
        assert False


def inflate(maze: list):
    newmaze = []
    for line in maze:
        newline = []
        for cell in line:
            if cell == "#":
                newline.extend(["#", "#"])
            elif cell == "O":
                newline.extend(["[", "]"])
            elif cell == ".":
                newline.extend([".", "."])
            elif cell == "@":
                newline.extend(["@", "."])
        newmaze.append(newline)
    return newmaze


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
        maze = []
        moves = []
        y = 0
        while line != "":  # The EOF char is an empty string
            line = line.rstrip()
            if line == "":
                loading = "MOVES"
                line = reader.readline()
                continue
            if loading == "MAZE":
                ml = [c for c in line]
                if "@" in ml:
                    robot = (ml.index("@"), y)
                maze.append(ml)
            elif loading == "MOVES":
                moves.extend(m for m in line)
            line = reader.readline()
            y += 1
        if DEBUG:
            for line in maze:
                print("".join(line))
            print(moves)
            print(robot)

        if args.part == 1:
            for idx, direction in enumerate(moves):
                if DEBUG:
                    print(idx, robot, direction)
                robot = move(cell=robot, maze=maze, direction=direction)
                if DEBUG:
                    for line in maze:
                        print("".join(line))
            result = 0
            for y, line in enumerate(maze):
                for x, cell in enumerate(line):
                    if cell == "O":
                        result += x + 100 * y
            print(result)
        else:
            maze = inflate(maze)
            for y, line in enumerate(maze):
                for x, cell in enumerate(line):
                    if cell == "@":
                        robot = (x, y)
            if DEBUG:
                for line in maze:
                    print("".join(line))
            for idx, direction in enumerate(moves):
                if DEBUG:
                    print(idx, robot, direction)
                robot = move(cell=robot, maze=maze, direction=direction)
                if DEBUG:
                    for line in maze:
                        print("".join(line))


if __name__ == "__main__":
    main()
