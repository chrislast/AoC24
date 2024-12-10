"""--- Day X:  ---"""
import numpy as np
import re
from utils import get_input, show, Map

DAY = X
INPUT = get_input(DAY)
#MAP = Map(INPUT.splitlines())
#H,W = MAP.img.height, MAP.img.width
#ARR = MAP.nparray()

def parse(line):
    pass

PARSED = [parse(line) for line in INPUT.splitlines()]

def p1():
    """ Day X: Part 1 """
    acc = 0
    return acc

def p2():
    """ Day X: Part 2 """
    acc = 0
    return acc

# expected results
p1.expects = 0
p2.expects = 0

# run functions
show(p1,p2)
