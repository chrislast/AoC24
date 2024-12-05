"""--- Day 4: Ceres Search ---"""
import numpy as np
import re
from utils import get_input, show, Map

INPUT = get_input(4)
WORDSEARCH = Map(INPUT.splitlines())
ARR = WORDSEARCH.nparray()
XMAS = b'XMAS'
X,M,A,S = XMAS

def xmas(x,y,dx,dy,idx):
    if idx == 4:
        return 1
    x += dx
    y += dy
    if not 0<=x<140 or not 0<=y<140:
        return 0
    if ARR[x,y] == XMAS[idx]:
        return xmas(x,y,dx,dy,idx+1)
    return 0

def p1():
    """
    Find "XMAS" in any direction
    """
    acc = 0
    width,height = ARR.shape
    for x in range(width):
        for y in range(height):
            if ARR[x,y] == X:
                acc += xmas(x,y,-1, 0,1)
                acc += xmas(x,y,-1,-1,1)
                acc += xmas(x,y, 0,-1,1)
                acc += xmas(x,y, 1, 0,1)
                acc += xmas(x,y, 1, 1,1)
                acc += xmas(x,y, 0, 1,1)
                acc += xmas(x,y,-1, 1,1)
                acc += xmas(x,y, 1,-1,1)
    return acc

def x_mas(x,y):
    if not 1<=x<139 or not 1<=y<139:
        return 0
    # compare unique cross-product to avoid sorting/reflecting/rotating
    if (ARR[x+1,y+1]*ARR[x-1,y-1] == M*S) and \
       (ARR[x-1,y+1]*ARR[x+1,y-1] == M*S):
        return 1
    return 0

def p2():
    """
    Find any rotated/reflected version of pattern
    M.S
    .A.
    M.S
    """
    acc = 0
    width,height = ARR.shape
    for x in range(width):
        for y in range(height):
            if ARR[x,y] == A:
                acc += x_mas(x,y)
    return acc


p1.expects = 2578
p2.expects = 1972
show(p1,p2)
