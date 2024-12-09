#!/usr/bin/env python3
from dataclasses import dataclass
from enum import Enum
from copy import deepcopy

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


def walk(labmap: list, guard: Guard, loopcheck: bool):
    g = Guard(0,0,Directions.NONE)
    g.x = guard.x
    g.y = guard.y
    g.direction = guard.direction
    lab = deepcopy(labmap)
    xlimit = len(lab[0])
    ylimit = len(lab)
    loop = False
    loopcount = 0
    while g.y >= 0 and g.y < ylimit and g.x >= 0 and g.x < xlimit:
        dx, dy = g.step()
        if g.y + dy >= 0 and g.y + dy < ylimit and g.x + dx >= 0 and g.x + dx < xlimit:
            lookup_cell = lab[g.y + dy][g.x + dx]
            if not lookup_cell.wall:
                g.y += dy
                g.x += dx
                if loopcheck and g.direction in lab[g.y][g.x].direction:
                    loop = True
                    break
                else:
                    lab[g.y][g.x].wall=True
                    _, isloop = walk(lab,guard,True)
                    if isloop:
                        loopcount+=1
                    lab[g.y][g.x].wall=False
                    lab[g.y][g.x].visited=True
                    lab[g.y][g.x].direction.append(g.direction)
            else:
                g.turn()
        else:
            break
    tot = 0
    for line in lab:
        tot += len([cell for cell in line if cell.visited==True])
    if loopcheck:
        return tot,loop
    else:
        return tot,loopcount

def main():
    with open("example", "r") as reader:
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
    tot,loop = walk(labmap,guard,False)
    print(tot,loop)


if __name__ == "__main__":
    main()
