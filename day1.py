"""day1.py"""
# pylint:disable=missing-function-docstring

from utils import get_input, show

INPUT = get_input(1).splitlines()
INPUT = [_.split() for _ in INPUT]
a = sorted([int(_[0]) for _ in INPUT])
b = sorted([int(_[1]) for _ in INPUT])

def p(func, exp=0):
    val = func()
    if val != exp:
        print(f"FAILED: got {val} expected {exp}")
    else:
        print(f"PASSED: {val}")

def p1():
    return sum(abs(b-a) for a,b in zip(a,b))

def p2():
    return sum(_*b.count(_) for _ in a)

p1.expects = 1651298
p2.expects = 21306195
show(p1,p2)
