"""--- Day 8: Resonant Collinearity ---"""
from itertools import combinations
from utils import get_input, show, Map

DAY = 8
INPUT = get_input(DAY)

MAP = Map(INPUT.splitlines())
H,W = MAP.img.height, MAP.img.width
ARR = MAP.nparray()

NODES = {}
ANTINODES = set()

for x in range(W):
    for y in range(H):
        nodetype = chr(ARR[y,x])
        if nodetype != ".":
            if nodetype not in NODES:
                NODES[nodetype] = []
            NODES[nodetype].append((x,y))

def add_antinodes1(node1,node2):
    x1,y1 = node1
    x2,y2 = node2
    dx,dy = x2-x1, y2-y1
    for ax,ay in (x1-dx,y1-dy),(x2+dx,y2+dy):
        if 0<=ax<W and 0<=ay<H:
            ANTINODES.add((ax,ay))

def add_antinodes2(node1, node2):
    ANTINODES.add(node1)
    ANTINODES.add(node2)
    x1,y1 = node1
    x2,y2 = node2
    dx,dy = x2-x1, y2-y1
    while True:
        x1 -= dx
        y1 -= dy
        if 0<=x1<W and 0<=y1<H:
            ANTINODES.add((x1,y1))
        else:
            break
    while True:
        x2 += dx
        y2 += dy
        if 0<=x2<W and 0<=y2<H:
            ANTINODES.add((x2,y2))
        else:
            break

def p1():
    """ Day 8: Part 1 """
    for xy in NODES.values():
        pairs = combinations(xy,2)
        for n1, n2 in pairs:
            add_antinodes1(n1,n2)
    return len(ANTINODES)

def p2():
    """ Day 8: Part 2 """
    for xy in NODES.values():
        pairs = combinations(xy,2)
        for n1, n2 in pairs:
            add_antinodes2(n1,n2)
    return len(ANTINODES)

# expected results
p1.expects = 228
p2.expects = 766

# run functions
show(p1,p2)
