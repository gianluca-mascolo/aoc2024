#!/usr/bin/env python3
import sys

class Disk:
    def __init__(self,dm: str):
        self.map = dm

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(dm={self.map!r})"

    def __str__(self):
        res = []
        for p,c in enumerate(self.map):
            repeat = int(c)
            if p % 2:
                res.append(f'{"."*repeat}')
            else:
                res.append(f'{str(p//2)*repeat}')
        return "".join(res)

def main():
    while line := sys.stdin.readline():
        disk = Disk(line.rstrip())
    print(disk)



if __name__ == "__main__":
    main()
