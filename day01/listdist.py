#!/usr/bin/env python3
def main():
    list_one = []
    list_two = []
    with open("input", "r") as reader:
        line = reader.readline()
        while line != "":  # The EOF char is an empty string
            line = line.rstrip()
            values = line.split(" ")
            list_one.append(int(values[0]))
            list_two.append(int(values[-1]))
            line = reader.readline()
    distance = sum(abs(a-b) for a,b in zip(sorted(list_one),sorted(list_two)))
    print(distance)
    similarity = sum(el*list_two.count(el) for el in list_one)
    print(similarity)

if __name__ == "__main__":
    main()
