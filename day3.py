"""--- Day 3: Mull It Over ---"""

import re
from utils import get_input, show

INPUT = get_input(3).splitlines()
INPUT = "#".join(INPUT)

# e.g. "mul(23,128)"
mulregex = re.compile(r"mul\((\d\d?\d?),(\d\d?\d?)\)")
# mul, do or don't command
cmdregex = re.compile(r"mul\(\d\d?\d?,\d\d?\d?\)|do\(\)|don't\(\)")

def p1():
    """sum all the valid mul()s"""
    muls = re.findall(mulregex,INPUT)
    return sum(int(x)*int(y) for x,y in muls)

def p2():
    """sum all the valid mul()s if do() is active"""
    acc = 0
    cmds = re.findall(cmdregex,INPUT)
    enabled = True
    for cmd in cmds:
        if cmd == "do()":
            enabled = True
        elif cmd == "don't()":
            enabled = False
        elif enabled:
            x,y = mulregex.match(cmd).groups()
            acc += int(x)*int(y)
    return acc

p1.expects = 166630675
p2.expects = 93465710
show(p1,p2)
