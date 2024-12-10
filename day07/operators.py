#!/usr/bin/env python3
import sys


def main():
    calibration = 0
    while line := sys.stdin.readline():
        line = line.rstrip()
        test_result = int(line.split(':')[0])
        input_numbers = [ int(n) for n in line.split(':')[1].split(' ')[1:] ]
        #print(test_result,input_numbers)
        num_op = len(input_numbers)-1
        operators = [ format(op,'b').zfill(num_op).replace('0','*').replace('1','+') for op in range(2**num_op) ]
        concat_operations = []
        for opnum,operations in enumerate(operators):
            concat_operations.append([])
            for pos,op in enumerate(operations):
                concat_operations[opnum].append(f"{input_numbers[pos]} {op} ")
            concat_operations[opnum].append(f"{input_numbers[-1]}")
        possible_results = []
        for q in concat_operations:
            query_string="".join(q)
            query = query_string.split(" ")
            acc = int(query[0])
            for k in range(len(query[1:])//2):
                evaluate="{accumulator} {operation} {value}".format(accumulator=str(acc),operation=query[2*k+1],value=query[2*k+2])
                acc = eval(evaluate)
            possible_results.append(acc)
        if test_result in possible_results:
            calibration+=test_result
    print(calibration)



if __name__ == "__main__":
    main()
