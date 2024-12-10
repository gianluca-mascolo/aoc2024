#!/usr/bin/env python3
import sys

DEBUG = False


def base3(i: int) -> str:
    r = str(i % 3)
    while i := i // 3:
        r = r + str(i % 3)
    return r[::-1]


def oplist(n: int):
    return [base3(op).zfill(n) for op in range(3**n)]


def main():
    calibration = [0, 0]
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
                elif op == "2":
                    DEBUG_STRING = DEBUG_STRING + f" || {input_numbers[pos+1]}"
                    acc = int(f"{acc}{input_numbers[pos+1]}")
                if acc > test_result:
                    break
            if test_result == acc:
                if DEBUG:
                    print(f"{DEBUG_STRING} = {acc}")
                if "||" in DEBUG_STRING:
                    calibration[1] += test_result
                else:
                    calibration[0] += test_result
                break
    print(calibration[0], sum(calibration))


if __name__ == "__main__":
    main()
