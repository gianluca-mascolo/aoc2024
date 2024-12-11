#!/usr/bin/env python3
import argparse
import sys
from dataclasses import dataclass

DEBUG = False


@dataclass
class File:
    id: int


class Disk:
    def __init__(self, dm: str):
        self.fat = []
        for position, content in enumerate(dm):
            self.fat
            repeat = int(content)
            if position % 2:
                self.fat.extend([None] * repeat)
            else:
                self.fat.extend([File(id=position // 2)] * repeat)
                self.filemax = position // 2
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
            for b in range(disk.size):
                if disk.fat[b] is None:
                    empty = b
                    break
            for b in range(disk.size - 1, 0, -1):
                if disk.fat[b] is not None:
                    full = b
                    break
            disk.fat[empty], disk.fat[full] = disk.fat[full], disk.fat[empty]
            if DEBUG:
                print(disk)
    elif method == 2:
        if None in disk.fat:
            for fileid in range(disk.filemax, -1, -1):
                filepos = disk.fat.index(File(fileid))
                move = []
                for q in range(filepos, disk.size):
                    if disk.fat[q] is not None and disk.fat[q].id == fileid:
                        move.append(q)
                    else:
                        break
                if DEBUG:
                    print(f"# id: {fileid} blocks: {len(move)} pos: {move}")
                empty = []
                is_moved = False
                for q in range(0, filepos):
                    if disk.fat[q] is None:
                        empty.append(q)
                    else:
                        if len(empty) >= len(move):
                            if DEBUG:
                                print(f"# move to {empty}")
                            for pos, block in enumerate(move):
                                disk.fat[empty[pos]], disk.fat[block] = disk.fat[block], disk.fat[empty[pos]]
                            is_moved = True
                            if DEBUG:
                                print(disk)
                            break
                        else:
                            empty.clear()
                if DEBUG and not is_moved:
                    print(f"# no contiguous free space for id: {fileid}")


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
    print(f"# {disk.checksum}")


if __name__ == "__main__":
    main()
