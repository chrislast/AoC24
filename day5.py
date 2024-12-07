"""--- Day 5: Print Queue ---"""
from utils import get_input, show

DAY = 5
INPUT = get_input(DAY)

rules = {}            # dictionary of sets - key must come before all items in set
list_of_updates = []  # puzzle inputs - list of lists of page updates

def parse():
    parsing_rules = True
    for line in INPUT.splitlines():
        if parsing_rules:
            if line == "":
                parsing_rules = False
                continue
            pre,post = [int(_) for _ in line.split("|")]

            if pre not in rules:
                rules[pre] = set()

            # add a rule
            rules[pre].add(post)
            continue

        # add list of updates
        list_of_updates.append([int(_) for _ in line.split(",")])

parse()

def p1():
    """ Day 5: Part 1 """
    acc = []
    for updates in list_of_updates:
        valid = True
        for pre, posts in rules.items():
            for post in posts:
                if post in updates and pre in updates:
                    if updates.index(post) < updates.index(pre):
                        valid = False
                        break
            if not valid:
                break

        if valid:
            acc.append(updates[len(updates)//2])

    return sum(acc)

def p2():
    """ Day 5: Part 2 """
    acc = []
    for updates in list_of_updates:
        fixes = 0
        # swapsort
        while True:
            fixes_applied = False
            for pre, posts in rules.items():
                for post in posts:
                    if post in updates and pre in updates:
                        i1, i2 = updates.index(post), updates.index(pre)
                        if i1 < i2:
                            # if items are not in correct order just swap them
                            updates[i2], updates[i1] = updates[i1], updates[i2]
                            fixes += 1
                            fixes_applied = True
            if not fixes_applied:
                break

        if fixes:
            acc.append(updates[len(updates)//2])

    return sum(acc)


# expected results
p1.expects = 5166
p2.expects = 4679

# run functions
show(p1,p2)
