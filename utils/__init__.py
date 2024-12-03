"""utils module"""
import sys
from pathlib import Path
import time
from types import SimpleNamespace
import random
import traceback

from PIL import Image
import numpy as np

from .download import download

# globals
NS = SimpleNamespace()
USING_EXAMPLE = len(sys.argv)>1

np.set_printoptions(threshold=np.inf)

TESTS = SimpleNamespace(
    FAILED = 0,
    PASSED = 0,
    EXECUTED = 0,
    ERRORS = 0,
    SKIPPED = 0)

def get_input(day, year=2024):
    pth = Path(f"day{day}.txt")
    if not pth.exists():
        download(day, year)
    return pth.read_text("ascii") if pth.exists() else ""

class Map:
    """
    DATA = get_input(15)
    m = Map(DATA)
    m.show()
    """
    def __init__(self, data, colorseed=0, output_size=None):
        height = len(data)
        width = max(len(_) for _ in data)
        self.img = Image.new("P", (width,height))
        if isinstance(data, np.ndarray):
            data = np.array(data, dtype=int)
            self.img.putdata(data.reshape(1,height*width)[0])
        else:
            for y in range(height):
                for x in range(width):
                    try:
                        self.set((x,y),data[y][x])
                    except IndexError:
                        continue
        random.seed(colorseed)
        #             black  + white + 254 randomized RGB colours
        self.palette=[0,0,0] + [255,255,255] + [random.randint(0,255) for _ in range(254*3)]
        self.img.putpalette(self.palette)
        self.gif = []
        self.output_size = output_size
        self.addtogif()

    def ival(self, val):
        # weirdly True is an int so test bool first!
        if isinstance(val, bool):
            return int(val)
        if isinstance(val, int):
            return val
        if isinstance(val, str) and len(val)==1:
            return ord(val)
        raise ValueError(f"{val}")

    def set(self, pos, val, out_of_range_is_error=True):
        """set pixel accepts int, bool, char"""
        val = self.ival(val)
        x, y = pos
        sx, sy = self.img.size
        if out_of_range_is_error or x<sx and y<sy:
            self.img.putpixel(pos,val)

    def get(self, pos):
        """get *integer* value
        cast it back to char or bool if needed"""
        return self.img.getpixel(pos)

    def resized(self):
        if not self.output_size:
            x,y = self.img.size
            while x<=200 and y<=200:
                x*=2
                y*=2
            self.output_size = (x,y)
        return self.img.copy().resize(self.output_size)

    def resize(self, scale_or_shape):
        x,y = self.img.size
        if isinstance(scale_or_shape, (int, float)):
            newx = int(x*scale_or_shape)
            newy = int(y*scale_or_shape)
            scale_or_shape = (newx,newy)
        return self.img.resize(scale_or_shape)

    def show(self):
        """show the PIL image"""
        self.resized().show()

    def save(self, *args, **kwargs):
        """save the PIL image"""
        self.resized().save(*args,**kwargs)

    def setcolour(self, val, rgb):
        """
        set a byte/bool/char representation to
        a fixed RGB value
        e.g.
          self.setcolour("#",(255,0,0))
          self.setcolour(".",(0,0,255))
        """
        val = self.ival(val)
        r, g, b = rgb
        self.palette[val*3+0] = r
        self.palette[val*3+1] = g
        self.palette[val*3+2] = b
        self.img.putpalette(self.palette)

    def addtogif(self):
        self.gif.append(self.resized())

    def savegif(self, fname, *, save_all=True, **kwargs):
        self.gif[0].save(fname, append_images=self.gif[1:], save_all=save_all, palette=self.palette, **kwargs)

        ##
        #
     #######
    ## # # ##
     #######

    SUBMARINE = [(0, -2), (1, -2), (0, -1), (-4, 1), (4, 1), # periscope and ends
                 *[(_,0) for _ in range(-3, 4)], # roof
                 *[(_,1) for _ in range(-3, 4, 2)], # walls
                 *[(_,2) for _ in range(-3, 4)]] # floor
    SUBMARINE_WINDOWS = [(-2, 1), (0, 1), (2, 1)]

    def add_a_submarine(self, x, y, body='@'):
        self.setcolour(body, (255,255,0)) # yellow (obviously)
        for sx, sy in self.SUBMARINE:
            self.set((x+sx,y+sy), body, out_of_range_is_error=False)
        for sx, sy in self.SUBMARINE_WINDOWS:
            self.set((x+sx,y+sy), 0, out_of_range_is_error=False)

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def show(*funcs, compact=False):
    part = 1
    for func in funcs:
        t1 = time.time()
        try:
            # resolve a solution
            ret = func()
        except Exception as exc:
            # catch any exception and replace it with a stacktrace
            ret = "    " + (''.join(traceback.format_exception(exc))).replace("\n","\n        ")
        elapsed = time.time()-t1
        if ret is None:
            TESTS.SKIPPED += 1
            return
        TESTS.EXECUTED += 1

        try:
            expect = func.expects
        except AttributeError:
            expect = None

        if expect:
            if ret == expect:
                txt = f"\n    Part {part}\n    PASS: {ret}\n    in {elapsed:.3f} seconds"
                print(txt.replace("\n    "," ") if compact else txt)
                TESTS.PASSED += 1
            else:
                txt = f"\n    Part {part}\n    FAIL: {ret} expected {expect}\n    in {elapsed:.3f} seconds"
                print(txt.replace("\n    "," ") if compact else txt)
                TESTS.FAILED += 1
        else:
            print(f"\n    Part {part}\n    {ret}\n    in {elapsed:.3f} seconds")
        if part==2:
            print("")
        part += 1

# Made a good guess at codes for 4x6 fonts used by AoC but incomplete data means I can't test most of them
ALPHA2CODE = dict(                                              # e.g.
    A=0x699f99, B=0xe9e99e, C=0x698896, D=0xe9999e, E=0xf8f88f, #  0 1 1 0 = 0x6
    F=0xf8e888, G=0x698b97, H=0x99f999, I=0xe4444e, J=0x311196, #  1 0 0 1 = 0x9
    K=0x9aca99, L=0x88888f, M=0x9f9999, N=0x9db999, O=0x699996, #  1 0 0 1 = 0x9
    P=0xe99e88, Q=0x6999a5, R=0xe99ea9, S=0x78611e, T=0xf44444, #  1 1 1 1 = 0xf
    U=0x999996, V=0x999952, W=0x9999f9, X=0x996999, Y=0x995222, #  1 0 0 1 = 0x9
    Z=0xf1248f)                                                 #  1 0 0 1 = 0x9 -> 0x699f99 = "A"
# reverse lookup table to convert a code to a character
CODE2ALPHA = {ALPHA2CODE[_]:_ for _ in ALPHA2CODE}
# assign a unique bit to each part of 4x6 font
ARRAY2CODE = np.array([1<<i for i in range(23,-1,-1)], dtype=int).reshape((6,4))

def decode4x6font(xypos):
    """
    Take a list of (x,y) coordinates and decode them to letters
    in Advent of Codes 6x4 font

    return the string matching the letters
    """
    txt = ""
    xl=[x for x,y in xypos]
    yl=[y for x,y in xypos]
    arr=np.zeros((max(yl)-min(yl)+1,max(xl)-min(xl)+1), dtype=int)
    for pos in xypos:
        arr[pos[::-1]] = 1
    # align text to top right of array
    line = arr[min(yl):,min(xl):]
    # extract characters until the line is empty
    while line.any():
        char = line[:6,:4]
        code = sum(sum(char*ARRAY2CODE))
        try:
            txt += CODE2ALPHA[code]
        except KeyError as err:
            print(f"Please add '{hex(code)}' ALPHA2CODE for:\n{char}")
            txt += "?"
        # cut the decoded character out of the array
        line = line[:,5:]
    return txt

def flatten(iterable):
    result = []
    iterable_types = (list,set,tuple) # ignore dict as it loses information
    for item in iterable:
        if isinstance(item, iterable_types):
            result += flatten(item)
        else:
            result.append(item)
    return tuple(result)

def batched(iterable, batch_size, strict=True, cast=None):
    """
    split an interable into batches of `batch_size` iterables
    e.g. batched("ABCDEFG",3,False) --> ["ABC","DEF","G"]
    """
    idx = 0
    batches = []
    while True:
        batch = iterable[idx:idx+batch_size]
        if not batch:
            break
        if strict:
            if len(batch) != batch_size:
                raise ValueError(
                    f"{batches}\n+ "
                    f"{batch}\nExpected {batch_size} elements not "
                    f"{len(batch)}")
        if cast:
            batch = cast(batch)
        batches.append(batch)
        idx += batch_size
    return batches
