#!/usr/bin/env python3
from dataclasses import dataclass
import sys

@dataclass
class File:
    id: int
    blocks: int

class Disk:
    def __init__(self, dm: str):
        self.map = dm
        self.fat = [ File(id=b//2,blocks=dm[b]) for b in range(0,len(dm),2) ]
        #self.blocks = [ for b in dm ]

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(dm={self.map!r})"

    def __str__(self):
        res = []
        for p, c in enumerate(self.map):
            repeat = int(c)
            if p % 2:
                res.append(f'{"."*repeat}')
            else:
                res.append(f"{str(p//2)*repeat}")
        return "".join(res)


def main():
    while line := sys.stdin.readline():
        disk = Disk(line.rstrip())
    print(disk)
    print(disk.fat)


if __name__ == "__main__":
    main()
