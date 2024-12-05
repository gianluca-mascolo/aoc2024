#!/usr/bin/env python3
import sys


def is_safe(level: list) -> bool:
    if level == sorted(level) or level == sorted(level, reverse=True):
        step = [abs(j - i) for i, j in zip(level[:-1], level[1:])]
        if all(map(lambda x: x >= 1 and x <= 3, step)):
            return True
    return False


def main():
    safe_levels = 0
    unsafe_levels = 0
    almost_safe = 0
    while line := sys.stdin.readline():
        line = line.rstrip()
        level = [int(el) for el in line.split(" ")]
        if is_safe(level):
            safe_levels += 1
        else:
            level_len = len(level)
            for e in range(level_len):
                if is_safe(level[0:e] + level[(e + 1) : level_len]):
                    almost_safe += 1
                    break
            unsafe_levels += 1
    print(f"safe: {safe_levels}")
    print(f"almost safe: {almost_safe}")
    print(f"total safe: {almost_safe+safe_levels}")
    print(f"unsafe: {unsafe_levels}")


if __name__ == "__main__":
    main()
