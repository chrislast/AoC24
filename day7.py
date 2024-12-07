"""--- Day 7: Bridge Repair ---"""
from utils import get_input, show
from functools import lru_cache

DAY = 7
INPUT = get_input(DAY)

def parse(line):
    testval, numbers = line.split(": ")
    numbers = [int(_) for _ in numbers.split()]
    return int(testval), numbers

PARSED = [parse(line) for line in INPUT.splitlines()]

def solve(tgt, acc, nums, use_concat_op=False):
    """
    Recursively try +, *, and optionally || operators at all positions
    in a list of numbers until we know whether the number
    list could ever equal the target
    """
    if acc>tgt:
        return False
    if nums:
        concat_result = False
        if use_concat_op:
            val = int(f"{acc}{nums[0]}")
            concat_result = solve(tgt, val, nums[1:], use_concat_op)
        return (concat_result or
                solve(tgt, acc+nums[0], nums[1:], use_concat_op) or
                solve(tgt, acc*nums[0], nums[1:], use_concat_op))
    if acc == tgt:
        return True
    return False

def p1():
    """ Day 7: Part 1
    + / * operators only
    """
    acc = 0
    for ans, nums in PARSED:
        if solve(ans,nums[0],tuple(nums[1:])):
            acc += ans
    return acc

def p2():
    """ Day 7: Part 2
    add the concatenate (||) operator to join two decimal numbers
    """
    acc = 0
    for ans, nums in PARSED:
        concval = int(f"{nums[0]}{nums[1]}")
        if (solve(ans, nums[0], tuple(nums[1:]), True) or
            solve(ans, concval, tuple(nums[2:]), True)):
            acc += ans
    return acc

# expected results
p1.expects = 4364915411363
p2.expects = 38322057216320

# run functions
show(p1, p2)
