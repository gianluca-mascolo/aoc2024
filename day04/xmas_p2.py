#!/usr/bin/env python3

def findcrossmas(matrix,x,y):
    xlimit = len(matrix[0])
    ylimit = len(matrix)
    if x+1 >= xlimit or x-1 < 0 or y+1 >= xlimit or y-1<0:
        return False
    cross_down = "".join(sorted(matrix[y-1][x-1]+matrix[y+1][x+1]))
    cross_up = "".join(sorted(matrix[y-1][x+1]+matrix[y+1][x-1]))
    if cross_down == 'MS' and cross_up == 'MS':
        return True
    return False
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
            if matrix[y][x] == 'A':
                if findcrossmas(matrix,x,y):
                    tot+=1
    print(tot)


if __name__ == "__main__":
    main()
