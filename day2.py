"""day 2"""

from utils import get_input, show

INPUT = get_input(2,2024)
LINES = INPUT.splitlines()

def p1():
    def safe(vals):
        for i in range(len(vals)-1):
            v1, v2 = vals[i:i+2]
            if not 1 <= (v2-v1) <= 3:
                return 0
        return 1
    acc = 0
    for _ in LINES:
        vals = [int(i) for i in _.split()]
        acc += safe(vals) or safe(vals[::-1])
    return acc


def p2():
    def safe(vals, dampened=False):
        for i in range(len(vals)-1):
            v1, v2 = vals[i:i+2]
            if not 1 <= (v2-v1) <= 3:
                if dampened:
                    return 0
                dampen_v1 = vals[:i+1]+vals[i+2:]
                dampen_v2 = vals[:i]+vals[i+1:]
                return safe(dampen_v1, True) or safe(dampen_v2, True)
        return 1
    acc = 0
    for _ in LINES:
        vals = [int(i) for i in _.split()]
        acc += safe(vals[:]) or safe(vals[::-1])
    return acc

p1.expects=526
p2.expects=566
show(p1,p2)
