"""Load Sokoban maps from file."""
# from core import GameMap
from os.path import dirname, abspath
import doctest


def printmap(mapobj):
    """helper function, intended to print loaded map object to the screen.

    # >>> t = LoadMaps("test_file.txt")
    # >>> t.printMap([['@', '#', ' ', '&', '#']])
    # [[1, 2, 3], [4, 5, 6]]
    """
    # iterable_map = iter(mapObj)
    for char in zip(mapobj):
        print("heh ", len(mapobj), char)


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
        """read string function, intended to load map object from string."""
        # todo na podstawie starpushera!
        level_num = 0
        map_text_lines = []  # contains the lines for a single level's map.
        map_obj = []  # the map object made from the data in map_text_lines
        for line_num in range(len(content)):
            # Process each line that was in the level file.
            line = content[line_num].rstrip('\r\n')

            if ';' in line:
                # Ignore the ; lines, they're comments in the level file.
                line = line[:line.find(';')]

            if line != '':
                # This line is part of the map.
                map_text_lines.append(line)
            elif line == '' and len(map_text_lines) > 0:
                # A blank line indicates the end of a level's map in the file.
                # Convert the text in map_text_lines into a level object.

                # Find the longest row in the map.
                max_width = -1
                for i in range(len(map_text_lines)):
                    if len(map_text_lines[i]) > max_width:
                        max_width = len(map_text_lines[i])
                # Add spaces to the ends of the shorter rows. This
                # ensures the map will be rectangular.
                for i in range(len(map_text_lines)):
                    map_text_lines[i] += ' ' * (max_width - len(map_text_lines[i]))

                # Convert map_text_lines to a map object.
                for x in range(len(map_text_lines[0])):
                    map_obj.append([])
                for y in range(len(map_text_lines)):
                    for x in range(max_width):
                        map_obj[x].append(map_text_lines[y][x])

                # Loop through the spaces in the map and find the @, ., and $
                # characters for the starting game state.
                startx = None  # The x and y for the player's starting position
                starty = None
                goals = []  # list of (x, y) tuples for each goal.
                stars = []  # list of (x, y) for each star's starting position.
                for x in range(max_width):
                    for y in range(len(map_obj[x])):
                        if map_obj[x][y] in ('@', '+'):
                            # '@' is player, '+' is player & goal
                            startx = x
                            starty = y
                        if map_obj[x][y] in ('.', '+', '*'):
                            # '.' is goal, '*' is star & goal
                            goals.append((x, y))
                        if map_obj[x][y] in ('$', '*'):
                            # '$' is star
                            stars.append((x, y))

                # Basic level design sanity checks:
                assert startx is not None and starty is not None, \
                    'Level %s (around line %s) in %s is missing a "@" or "+" to mark the start.' % (
                        level_num + 1, line_num, self.source)
                assert len(goals) > 0, \
                    'Level %s (around line %s) in %s must have at least one goal.' % (
                        level_num + 1, line_num, self.source)
                assert len(stars) >= len(goals), \
                    'Level %s (around line %s) in %s is impossible to solve.' \
                    'It has %s goals but only %s stars.' % (
                        level_num + 1, line_num, self.source, len(goals), len(stars))

                # Create level object and starting game state object.
                game_state_obj = {'player': (startx, starty),
                                  'stepCounter': 0,
                                  'stars': stars}
                level_obj = {'width': max_width,
                             'height': len(map_obj),
                             'map_obj': map_obj,
                             'goals': goals,
                             'start_state': game_state_obj}

                self.levels.append(level_obj)

                # Reset the variables for reading the next map.
                map_text_lines = []
                map_obj = []
                # game_state_obj = {}
                level_num += 1

                # return self.printMap(self.levels[0]['map_obj'])


doctest.testmod()
