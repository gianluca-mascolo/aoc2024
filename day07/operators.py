#!/usr/bin/env python3
import sys

DEBUG = False


def oplist(n: int):
    return [format(op, "b").zfill(n) for op in range(2**n)]


def main():
    calibration = 0
    while line := sys.stdin.readline():
        line = line.rstrip()
        test_result = int(line.split(":")[0])
        input_numbers = [int(n) for n in line.split(":")[1].split(" ")[1:]]
        if DEBUG:
            print("test:{} values:{}".format(test_result, input_numbers))
        num_op = len(input_numbers) - 1
        operators = oplist(num_op)
        for operations in operators:
            acc = input_numbers[0]
            DEBUG_STRING = str(acc)
            for pos, op in enumerate(operations):
                if op == "0":
                    DEBUG_STRING = DEBUG_STRING + f" * {input_numbers[pos+1]}"
                    acc *= input_numbers[pos + 1]
                elif op == "1":
                    DEBUG_STRING = DEBUG_STRING + f" + {input_numbers[pos+1]}"
                    acc += input_numbers[pos + 1]
                if acc > test_result:
                    break
            if test_result == acc:
                if DEBUG:
                    print(f"{DEBUG_STRING} = {acc}")
                calibration += test_result
                break
    print(calibration)


if __name__ == "__main__":
    main()
