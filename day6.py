"""--- Day X: Guard Gallivant ---"""
import numpy as np
from collections import Counter
from utils import get_input, show, Map

DAY = 6
INPUT = get_input(DAY)
MAP = Map(INPUT.splitlines())
WIDTH, HEIGHT = MAP.img.size

#MAP.show()
ARR = MAP.nparray()

GUARD = np.where(ARR == ord('^'))
GUARD = int(GUARD[1][0]), int(GUARD[0][0])

# right turn dx,dy sequence
TURN_RIGHT = [(0,-1), (1,0), (0,1), (-1,0)]
X = ord("X")
PATH = []
GIF1 = [MAP.img.copy()]

print(GUARD)
def p1():
    """ Day 6: Part 1 """
    x,y = GUARD
    tidx = 0
    while True:
        GIF1.append(MAP.img.copy())
        MAP.set((x,y),X)
        # stop if we reached edge of map
        if x==0 or y==0 or x==WIDTH-1 or y==HEIGHT-1:
            break
        nx = TURN_RIGHT[tidx][0] + x
        ny = TURN_RIGHT[tidx][1] + y
        if MAP.get((nx,ny)) == ord("#"):
            tidx = (tidx + 1) & 3 # turn right
        else:
            x,y = nx, ny # move forward
            PATH.append((x,y))

    return Counter(MAP.img.getdata())[X]

GIF2 = []
def p2():
    """ Day 6: Part 2 """
    acc = 0
    # If we didn't reach a position in the first map, then there's no point
    # putting an obstacle there so just place obstacles at each point on the way
    tried = set()
    for obstacle in PATH:
        if obstacle in tried:
            continue
        tried.add(obstacle)
        seen = set()
        # reset the map and guard, add the new obstacle
        map2 = Map(ARR)
        map2.set(obstacle, ord("#"))
        x,y = guard = GUARD
        map2.set(guard, X)
        tidx = 0
        while True:
            if x==0 or y==0 or x==WIDTH-1 or y==HEIGHT-1:
                break

            newpos = (TURN_RIGHT[tidx][0] + x,
                      TURN_RIGHT[tidx][1] + y)

            val = map2.get(newpos)
            if val == ord("#"):
                # turn
                tidx = (tidx + 1) & 3
            else:
                 # encode position + direction
                hsh = hash((newpos,tidx))
                # if we've done this before add a valid obstacle and stop
                if hsh in seen:
                    acc += 1
                    GIF2.append(map2.img)
                    break
                # otherwise remember and go forward
                map2.set(newpos, X)
                seen.add(hsh)
                x,y = newpos
    return acc

# expected results
p1.expects = 5534
p2.expects = 2262

# run functions
show(p1,p2)

GIF1[0].save("day6a.gif", append_images=GIF1[1:], save_all=True)
GIF2[0].save("day6b.gif", append_images=GIF2[1:], save_all=True)
