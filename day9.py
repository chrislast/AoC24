"""--- Day X:  ---"""
import numpy as np
import re
from utils import get_input, show, Map
from collections import deque

DAY = 9
INPUT = get_input(DAY).strip()
INPxUT = "2333133121414131402"
#MAP = Map(INPUT.splitlines())
#ARR = MAP.nparray()

DISK = []
ID = 0
MAP = {}
DISKPOS = 0
TXT = ""

FILE = True
for c in INPUT:
    c = int(c)
    if FILE:
        MAP[ID] = DISKPOS
        DISKPOS += c
        TXT += f"{ID%10}" * c
        DISK += [ID] * c
        FILE = False
        ID += 1
    else: # gap
        DISKPOS += c
        TXT += "." * c
        DISK += [None] * c
        FILE = True

#print(MAP)

def p1():
    """ Day X: Part 1 """
    disk = DISK.copy()
    pos = 0
    while True:
        try:
            while disk[pos] is not None:
                pos += 1
        except IndexError:
            break
        disk[pos] = disk[-1]
        pos += 1
        del disk[-1]
        while disk[-1] is None:
            del disk[-1]

    acc = 0
    for i, v in enumerate(disk):
        acc += i*v
    return acc

def p2():
    """ Day X: Part 2 """
    acc = 0
    return acc

# expected results
p1.expects = 6471961544878
p2.expects = 0

# run functions
show(p1,p2)
