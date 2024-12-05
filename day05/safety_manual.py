#!/usr/bin/env python3
import sys


def ordering(update, rules):
    pages = [p for p in update]
    valid = True
    correct = None
    for k, v in enumerate(pages):
        if breaking_rules := (set(pages[:k]) & set(rules[v]["before"])):
            valid = False
            violate = breaking_rules.pop()
            swap = pages.index(violate)
            pages[k], pages[swap] = pages[swap], pages[k]
            correct = ordering(pages, rules)
            break
        if breaking_rules := (set(pages[k + 1 :]) & set(rules[v]["after"])):
            valid = False
            violate = breaking_rules.pop()
            swap = pages.index(violate)
            pages[k], pages[swap] = pages[swap], pages[k]
            correct = ordering(pages, rules)
            break
    if valid:
        return pages[len(pages) // 2]
    return correct


def main():
    loading = "rule"
    rules = {}
    part1 = 0
    part2 = 0
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
                    correct = ordering(update, rules)
                    part2 += correct
                    print(f"correct: {correct}")
                    break
            print(f"update valid: {valid}")
            if valid:
                part1 += update[len(update) // 2]
    print(part1, part2)


if __name__ == "__main__":
    main()
