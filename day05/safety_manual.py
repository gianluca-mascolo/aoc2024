#!/usr/bin/env python3
import sys


def main():
    loading = "rule"
    rules = {}
    tot = 0
    while line := sys.stdin.readline():
        line = line.rstrip()
        if line == "":
            loading = "update"
            continue
        if loading == "rule":
            rule = [int(n) for n in line.split("|")]
            for r in rule:
                if r not in rules.keys():
                    rules[r] = {"before": [], "after": []}
            rules[rule[0]]["before"].append(rule[1])
            rules[rule[1]]["after"].append(rule[0])
        elif loading == "update":
            update = [int(n) for n in line.split(",")]
            print(f"checking update {update}")
            valid = True
            for k, v in enumerate(update):
                if (set(update[:k]) & set(rules[v]["before"])) or (set(update[k + 1 :]) & set(rules[v]["after"])):
                    valid = False
                    break
            print(f"update valid: {valid}")
            if valid:
                tot += update[len(update) // 2]
    print(tot)


if __name__ == "__main__":
    main()
