#!/usr/bin/env python3
def findxmas(matrix, x, y):
    xlimit = len(matrix[0])
    ylimit = len(matrix)
    limit = max(xlimit, ylimit)
    test = []
    test.append(matrix[y][x : x + 4])
    test.append(matrix[y][x - 3 : x + 1])
    vline = "".join(line[x] for line in matrix)
    test.append(vline[y : y + 4])
    test.append(vline[y - 3 : y + 1])
    diagonal_up = []
    diagonal_down = []
    for delta in range(-1 * limit, limit):
        if delta == 0:
            diagonal_down.append(".")
            diagonal_up.append(".")
        if delta != 0 and x + delta >= 0 and y + delta >= 0 and x + delta < xlimit and y + delta < ylimit:
            diagonal_down.append(matrix[y + delta][x + delta])
        if delta != 0 and x + delta >= 0 and y - delta >= 0 and x + delta < xlimit and y - delta < ylimit:
            diagonal_up.append(matrix[y - delta][x + delta])
    diagonal_up = "".join(diagonal_up)
    diagonal_down = "".join(diagonal_down)
    pivot = diagonal_up.find(".")
    test.append(diagonal_up[pivot : pivot + 4].replace(".", "X"))
    test.append(diagonal_up[pivot - 3 : pivot + 1].replace(".", "X"))
    pivot = diagonal_down.find(".")
    test.append(diagonal_down[pivot : pivot + 4].replace(".", "X"))
    test.append(diagonal_down[pivot - 3 : pivot + 1].replace(".", "X"))
    return test.count("XMAS") + test.count("SAMX")


def main():
    matrix = []
    with open("input", "r") as reader:
        line = reader.readline()
        while line != "":  # The EOF char is an empty string
            line = line.rstrip()
            matrix.append(line)
            line = reader.readline()
    tot = 0
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] == "X":
                num = findxmas(matrix, x, y)
                tot += num
    print(tot)


if __name__ == "__main__":
    main()
