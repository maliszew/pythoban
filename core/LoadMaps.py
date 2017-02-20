"""Load Sokoban maps from file."""
import numpy
# from core import GameMap
from os.path import dirname, abspath


class LoadMaps:
    def __init__(self, source):
        self.levels = []
        self.source = source

    def read_file(self):
        """assumption: each level in file ends with a blank line.
        each levels file needs to be stored in /assets/ folder.

        >>> t1 = LoadMaps("starPusherLevels.txt")
        >>> t1.read_file()
        >>> t1.levels.__len__()
        201

        >>> t2 = LoadMaps("microban.xsb")
        >>> t2.read_file()
        >>> t2.levels.__len__()
        153

        >>> t3 = LoadMaps("sokoban.txt")
        >>> t3.read_file()
        >>> t3.levels.__len__()
        50
        """
        # assert numpy.os.path.exists(self.source), 'Cannot find the level file: %s' % (self.source)
        parent_dir = dirname(dirname(abspath(__file__)))
        map_dir = parent_dir + "/assets/" + self.source
        file = open(map_dir, 'r')
        content = file.readlines() + ['\r\n']
        file.close()
        self.read_string(content)

    def read_string(self, content):
        """read string function, intended to load map object from string.

        # >>> t = LoadMaps("test_file.txt")
        # >>> t.read_string("## **   @#\\n##  &&   #")
        # \#\# **   @\#
        # \#\#  &&   \#
        #
        # >>> s = "#######\\n#     #\\n#     #\\n#. #  #\\n#. $$ #\\n#.$$  #\\n#.#  @#\\n#######"
        # >>> t2 = LoadMaps("test_file.txt")
        # >>> t2.read_string(s)
        # \#\#\#$$$$
        """
        #todo na podstawie starpushera!
        levelNum = 0
        mapTextLines = []  # contains the lines for a single level's map.
        mapObj = []  # the map object made from the data in mapTextLines
        for lineNum in range(len(content)):
            # Process each line that was in the level file.
            line = content[lineNum].rstrip('\r\n')

            if ';' in line:
                # Ignore the ; lines, they're comments in the level file.
                line = line[:line.find(';')]

            if line != '':
                # This line is part of the map.
                mapTextLines.append(line)
            elif line == '' and len(mapTextLines) > 0:
                # A blank line indicates the end of a level's map in the file.
                # Convert the text in mapTextLines into a level object.

                # Find the longest row in the map.
                maxWidth = -1
                for i in range(len(mapTextLines)):
                    if len(mapTextLines[i]) > maxWidth:
                        maxWidth = len(mapTextLines[i])
                # Add spaces to the ends of the shorter rows. This
                # ensures the map will be rectangular.
                for i in range(len(mapTextLines)):
                    mapTextLines[i] += ' ' * (maxWidth - len(mapTextLines[i]))

                # Convert mapTextLines to a map object.
                for x in range(len(mapTextLines[0])):
                    mapObj.append([])
                for y in range(len(mapTextLines)):
                    for x in range(maxWidth):
                        mapObj[x].append(mapTextLines[y][x])

                # Loop through the spaces in the map and find the @, ., and $
                # characters for the starting game state.
                startx = None  # The x and y for the player's starting position
                starty = None
                goals = []  # list of (x, y) tuples for each goal.
                stars = []  # list of (x, y) for each star's starting position.
                for x in range(maxWidth):
                    for y in range(len(mapObj[x])):
                        if mapObj[x][y] in ('@', '+'):
                            # '@' is player, '+' is player & goal
                            startx = x
                            starty = y
                        if mapObj[x][y] in ('.', '+', '*'):
                            # '.' is goal, '*' is star & goal
                            goals.append((x, y))
                        if mapObj[x][y] in ('$', '*'):
                            # '$' is star
                            stars.append((x, y))

                # Basic level design sanity checks:
                assert startx != None and starty != None, 'Level %s (around line %s) in %s is missing a "@" or "+" to mark the start point.' % (
                levelNum + 1, lineNum, self.source)
                assert len(goals) > 0, 'Level %s (around line %s) in %s must have at least one goal.' % (
                levelNum + 1, lineNum, self.source)
                assert len(stars) >= len(
                    goals), 'Level %s (around line %s) in %s is impossible to solve. It has %s goals but only %s stars.' % (
                levelNum + 1, lineNum, self.source, len(goals), len(stars))

                # Create level object and starting game state object.
                gameStateObj = {'player': (startx, starty),
                                'stepCounter': 0,
                                'stars': stars}
                levelObj = {'width': maxWidth,
                            'height': len(mapObj),
                            'mapObj': mapObj,
                            'goals': goals,
                            'startState': gameStateObj}

                self.levels.append(levelObj)

                # Reset the variables for reading the next map.
                mapTextLines = []
                mapObj = []
                gameStateObj = {}
                levelNum += 1

        # return self.printMap(self.levels[0]['mapObj'])

    def printMap(self, mapObj):
        """helper function, intended to print loaded map object to the screen.

        # >>> t = LoadMaps("test_file.txt")
        # >>> t.printMap([['@', '#', ' ', '&', '#']])
        # [[1, 2, 3], [4, 5, 6]]
        """
        iterable_map = iter(mapObj)
        for char in zip(mapObj):
            print("heh ", len(mapObj), char)

import doctest
doctest.testmod()
