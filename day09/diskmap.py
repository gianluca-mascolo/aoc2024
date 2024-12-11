#!/usr/bin/env python3
import argparse
import sys
from dataclasses import dataclass

DEBUG = False


@dataclass
class File:
    id: int
    blocks: int


class Disk:
    def __init__(self, dm: str):
        self.fat = []
        for position, content in enumerate(dm):
            self.fat
            repeat = int(content)
            if position % 2:
                self.fat.extend([None] * repeat)
            else:
                self.fat.extend([File(id=position // 2, blocks=repeat)] * repeat)
        self.size = len(self.fat)

    @property
    def compacted(self) -> bool:
        if None in self.fat:
            empty = self.fat.index(None)
            return all(b is None for b in self.fat[empty:])
        else:
            return True

    @property
    def checksum(self) -> int:
        return sum(b * self.fat[b].id for b in range(self.size) if self.fat[b])

    def __str__(self):
        return "".join([str(b.id) if b else "." for b in self.fat])


def defrag(disk: Disk, method: int):
    if method == 1:
        while not disk.compacted:
            size = disk.size
            for b in range(size):
                if disk.fat[b] is None:
                    empty = b
                    break
            for b in range(size - 1, 0, -1):
                if disk.fat[b] is not None:
                    full = b
                    break
            disk.fat[empty], disk.fat[full] = disk.fat[full], disk.fat[empty]
            if DEBUG:
                print(disk)
    elif method == 2:
        return True


def main():
    global DEBUG
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Debug ouput", action="store_true")
    parser.add_argument("-p", "--part", type=int, help="part to solve (1 or 2)", default=1)
    args = parser.parse_args()
    if args.debug:
        DEBUG = True
    assert args.part in [1, 2]
    while line := sys.stdin.readline():
        disk = Disk(line.rstrip())
    if DEBUG:
        print(disk)
    defrag(disk, args.part)
    print(disk.checksum)


if __name__ == "__main__":
    main()
