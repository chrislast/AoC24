"""--- Day 10: Hoof It ---"""
from utils import get_input, show, Map

DAY = 10
INPUT = get_input(DAY)

MAP = Map(INPUT.splitlines())
H,W = MAP.img.height, MAP.img.width

def trails(x,y,z,seen):
    """recursively climb a hill [0-9]"""
    # check we are still on the map
    if x<0 or y<0 or x>=W or y>=H:
        return 0

    height = MAP.get((x,y))-ord("0")
    # check we have climbed by exactly 1
    if height != z:
        return 0

    # check if we have reached a trail end
    if height == 9:
        # in part 1 we only count unique trail ends from trailheads
        # in part 2 (seen==None) all routes are counted
        if seen is not None:
            if (x,y) in seen:
                return 0 # found non-unique trail end
            seen.add((x,y))
        return 1

    # if not try to climb in all N,S,E,W directions
    return (trails(x-1,y,z+1,seen) +
            trails(x+1,y,z+1,seen) +
            trails(x,y-1,z+1,seen) +
            trails(x,y+1,z+1,seen))

def p1():
    """ Day 10: Part 1 """
    acc = 0
    for x in range(W):
        for y in range(H):
            acc += trails(x,y,0,set())
    return acc

def p2():
    """ Day 10: Part 2 """
    acc = 0
    for x in range(W):
        for y in range(H):
            acc += trails(x,y,0,None)
    return acc

# expected results
p1.expects = 638
p2.expects = 1289

# run functions
show(p1,p2)
