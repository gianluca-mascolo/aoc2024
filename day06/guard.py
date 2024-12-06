#!/usr/bin/env python3
from dataclasses import dataclass
from enum import Enum


class Directions(Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"
    NONE = None

WALL = { "#": True, ".": False }

@dataclass
class Guard:
    x: int
    y: int
    direction: Directions

    def step(self):
        if self.direction == Directions.UP:
            return 0, -1
        elif self.direction == Directions.DOWN:
            return 0, 1
        elif self.direction == Directions.LEFT:
            return -1, 0
        elif self.direction == Directions.RIGHT:
            return 1, 0

    def turn(self):
        if self.direction == Directions.UP:
            self.direction = Directions.RIGHT
        elif self.direction == Directions.DOWN:
            self.direction = Directions.LEFT
        elif self.direction == Directions.LEFT:
            self.direction = Directions.UP
        elif self.direction == Directions.RIGHT:
            self.direction = Directions.DOWN

@dataclass
class Cell():
    wall: bool
    visited: bool
    direction: list

def main():
    with open("input", "r") as reader:
        line = reader.readline()
        y = 0
        labmap = []
        while line != "":  # The EOF char is an empty string
            labmap.append([])
            line = line.rstrip()
            x = 0
            for cell in line:
                if cell in [d.value for d in Directions]:
                    labmap[y].append(Cell(wall=False,visited=True,direction=[Directions(cell)]))
                    guard = Guard(x, y, Directions(cell))
                else:
                    labmap[y].append(Cell(wall=WALL[cell],visited=False,direction=[]))
                x += 1
            line = reader.readline()
            y += 1
    xlimit = len(labmap[0])
    ylimit = len(labmap)
    while guard.y >= 0 and guard.y < ylimit and guard.x >= 0 and guard.x < xlimit:
        dx, dy = guard.step()
        if guard.y + dy >= 0 and guard.y + dy < ylimit and guard.x + dx >= 0 and guard.x + dx < xlimit:
            lookup_cell = labmap[guard.y + dy][guard.x + dx]
            if not lookup_cell.wall:
                guard.y += dy
                guard.x += dx
                labmap[guard.y][guard.x].visited=True
                labmap[guard.y][guard.x].direction.append(guard.direction)
            else:
                guard.turn()
        else:
            break
    tot = 0
    for line in labmap:
        tot += len([cell for cell in line if cell.visited==True])
    print(tot)


if __name__ == "__main__":
    main()
