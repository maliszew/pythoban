"""simple level solver.
based on http://rosettacode.org/wiki/Sokoban """

from array import array
from collections import deque


def init(board):
    global data, nrows, sdata, ddata, px, py
    data = []
    nrows = 0
    px = py = 0
    sdata = ""
    ddata = ""

    data = filter(None, board.splitlines())
    nrows = max(len(r) for r in data)

    maps = {' ': ' ', '.': '.', '@': ' ', '#': '#', '$': ' '}
    mapd = {' ': ' ', '.': ' ', '@': '@', '#': ' ', '$': '*'}

    for r, row in enumerate(data):
        for c, ch in enumerate(row):
            sdata += maps[ch]
            ddata += mapd[ch]
            if ch == '@':
                px = c
                py = r


def push(x, y, dx, dy, level_data):
    if sdata[(y + 2 * dy) * nrows + x + 2 * dx] == '#' or \
                    level_data[(y + 2 * dy) * nrows + x + 2 * dx] != ' ':
        return None

    data2 = array("c", level_data)
    data2[y * nrows + x] = ' '
    data2[(y + dy) * nrows + x + dx] = '@'
    data2[(y + 2 * dy) * nrows + x + 2 * dx] = '*'
    return data2.tostring()


def is_solved(level_data):
    for i in xrange(len(level_data)):
        if (sdata[i] == '.') != (level_data[i] == '*'):
            return False
    return True


def solve():
    open_level = deque([(ddata, "", px, py)])
    visited = {ddata}
    dirs = ((0, -1, 'u', 'U'), (1, 0, 'r', 'R'),
            (0, 1, 'd', 'D'), (-1, 0, 'l', 'L'))

    lnrows = nrows
    while open_level:
        cur, csol, x, y = open_level.popleft()

        for di in dirs:
            temp = cur
            dx, dy = di[0], di[1]

            # print("temp", x, dx, y, dy, lnrows, ((y + dy) * lnrows + x + dx), temp)
            if temp[(y + dy) * lnrows + x + dx] == '*':
                temp = push(x, y, dx, dy, temp)
                if temp and temp not in visited:
                    if is_solved(temp):
                        return csol + di[3]
                    open_level.append((temp, csol + di[3], x + dx, y + dy))
                    visited.add(temp)
            else:
                # print("sdata", x, dx, y, dy, lnrows, ((y + dy) * lnrows + x + dx), sdata)
                if sdata[(y + dy) * lnrows + x + dx] == '#' or \
                                temp[(y + dy) * lnrows + x + dx] != ' ':
                    continue

                data2 = array("c", temp)
                data2[y * lnrows + x] = ' '
                data2[(y + dy) * lnrows + x + dx] = '@'
                temp = data2.tostring()

                if temp not in visited:
                    if is_solved(temp):
                        return csol + di[2]
                    open_level.append((temp, csol + di[2], x + dx, y + dy))
                    visited.add(temp)

    return "No solution"


level = """\
#######
#     #
#     #
#. #  #
#. $$ #
#.$$  #
#.#  @#
#######"""


# init(level)
# print(level, "\n\n", solve())

def run(level_string):
    print("Solving...")
    # print(level_string)
    init(level_string)
    return solve()
