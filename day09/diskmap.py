#!/usr/bin/env python3
import sys
from dataclasses import dataclass


@dataclass
class File:
    id: int
    blocks: int


class Disk:
    def __init__(self, dm: str):
        self.map = dm
        self.fat = []
        for position, content in enumerate(dm):
            self.fat
            repeat = int(content)
            if position % 2:
                self.fat.extend([None] * repeat)
            else:
                self.fat.extend([File(id=position // 2, blocks=repeat)] * repeat)
    
    def compacted(self):
        if None in self.fat:
            empty = self.fat.index(None)
            return all(b == None for b in self.fat[empty:])
        else:
            return True

    def __str__(self):
        return "".join([str(b.id) if b else "." for b in self.fat])


def main():
    while line := sys.stdin.readline():
        disk = Disk(line.rstrip())
    # print(disk)
    # for b in disk.fat:
    #     print(b)
    print(disk)
    print(disk.compacted())


if __name__ == "__main__":
    main()
