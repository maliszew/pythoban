"""Draws previously loaded map on the screen."""

import copy
import pygame
import random

from core import SolveMap

# global FPSCLOCK, DISPLAYSURF, IMAGESDICT, TILEMAPPING, OUTSIDEDECOMAPPING, BASICFONT, PLAYERIMAGES, currentImage

FPS = 30  # frames per second to update the screen
WINWIDTH = 1200  # width of the program's window, in pixels
WINHEIGHT = 600  # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

# The total width and height of each tile in pixels.
TILEWIDTH = 50
TILEHEIGHT = 85
TILEFLOORHEIGHT = 40

CAM_MOVE_SPEED = 1  # how many pixels per frame the camera moves

# The percentage of outdoor tiles that have additional
# decoration on them, such as a tree or rock.
OUTSIDE_DECORATION_PCT = 20

BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

IMAGESDICT = {'uncovered goal': pygame.image.load('assets/RedSelector.png'),
              'covered goal': pygame.image.load('assets/Selector.png'),
              'star': pygame.image.load('assets/Star.png'),
              'corner': pygame.image.load('assets/Wall_Block_Tall.png'),
              'wall': pygame.image.load('assets/Wood_Block_Tall.png'),
              'inside floor': pygame.image.load('assets/Plain_Block.png'),
              'outside floor': pygame.image.load('assets/Grass_Block.png'),
              'title': pygame.image.load('assets/star_title.png'),
              'solved': pygame.image.load('assets/star_solved.png'),
              'princess': pygame.image.load('assets/princess.png'),
              'boy': pygame.image.load('assets/boy.png'),
              'catgirl': pygame.image.load('assets/catgirl.png'),
              'horngirl': pygame.image.load('assets/horngirl.png'),
              'pinkgirl': pygame.image.load('assets/pinkgirl.png'),
              'rock': pygame.image.load('assets/Rock.png'),
              'short tree': pygame.image.load('assets/Tree_Short.png'),
              'tall tree': pygame.image.load('assets/Tree_Tall.png'),
              'ugly tree': pygame.image.load('assets/Tree_Ugly.png')}

TILEMAPPING = {'x': IMAGESDICT['corner'],
               '#': IMAGESDICT['wall'],
               'o': IMAGESDICT['inside floor'],
               ' ': IMAGESDICT['outside floor']}
OUTSIDEDECOMAPPING = {'1': IMAGESDICT['rock'],
                      '2': IMAGESDICT['short tree'],
                      '3': IMAGESDICT['tall tree'],
                      '4': IMAGESDICT['ugly tree']}

currentImage = 0
PLAYERIMAGES = [IMAGESDICT['princess'],
                IMAGESDICT['boy'],
                IMAGESDICT['catgirl'],
                IMAGESDICT['horngirl'],
                IMAGESDICT['pinkgirl']]

BRIGHTBLUE = (0, 170, 255)
WHITE = (255, 255, 255)
BGCOLOR = BRIGHTBLUE
TEXTCOLOR = WHITE

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


# solution = ""


def drawmap(map_obj, game_state_obj, goals):
    """Draws the map to a Surface object, including the player and
    stars. This function does not call pygame.display.update(), nor
    does it draw the "Level" and "Steps" text in the corner."""

    # map_surf will be the single Surface object that the tiles are drawn
    # on, so that it is easy to position the entire map on the DISPLAYSURF
    # Surface object. First, the width and height must be calculated.
    map_surf_width = len(map_obj) * TILEWIDTH
    map_surf_height = (len(map_obj[0]) - 1) * TILEFLOORHEIGHT + TILEHEIGHT
    map_surf = pygame.Surface((map_surf_width, map_surf_height))
    map_surf.fill(BGCOLOR)  # start with a blank color on the surface.

    # Draw the tile sprites onto this surface.
    for x in range(len(map_obj)):
        for y in range(len(map_obj[x])):
            space_rect = pygame.Rect((x * TILEWIDTH, y * TILEFLOORHEIGHT, TILEWIDTH, TILEHEIGHT))
            if map_obj[x][y] in TILEMAPPING:
                base_tile = TILEMAPPING[map_obj[x][y]]
            else:  # elif map_obj[x][y] in OUTSIDEDECOMAPPING:
                base_tile = TILEMAPPING[' ']

            # First draw the base ground/wall tile.
            map_surf.blit(base_tile, space_rect)

            if map_obj[x][y] in OUTSIDEDECOMAPPING:
                # Draw any tree/rock decorations that are on this tile.
                map_surf.blit(OUTSIDEDECOMAPPING[map_obj[x][y]], space_rect)
            elif (x, y) in game_state_obj['stars']:
                if (x, y) in goals:
                    # A goal AND star are on this space, draw goal first.
                    map_surf.blit(IMAGESDICT['covered goal'], space_rect)
                # Then draw the star sprite.
                map_surf.blit(IMAGESDICT['star'], space_rect)
            elif (x, y) in goals:
                # Draw a goal without a star on it.
                map_surf.blit(IMAGESDICT['uncovered goal'], space_rect)

            # Last draw the player on the board.
            if (x, y) == game_state_obj['player']:
                # Note: The value "currentImage" refers
                # to a key in "PLAYERIMAGES" which has the
                # specific player image we want to show.
                map_surf.blit(PLAYERIMAGES[currentImage], space_rect)

    return map_surf


def runlevel(levels, level_num):
    pygame.init()
    global currentImage
    level_obj = levels[level_num]
    map_obj = decoratemap(level_obj['map_obj'], level_obj['start_state']['player'])
    game_state_obj = copy.deepcopy(level_obj['start_state'])
    map_needs_redraw = True  # set to True to call drawmap()
    level_surf = BASICFONT.render(
        'Level %s of %s. N / B = Next / Back level. WSAD - move camera.' % (level_num + 1, len(levels)), 1, TEXTCOLOR)
    level_rect = level_surf.get_rect()
    level_rect.bottomleft = (20, WINHEIGHT - 60)
    info_surf = BASICFONT.render('Too hard? C = Cheat and solve it! ESC = restart current level.', 1, TEXTCOLOR)
    info_rect = info_surf.get_rect()
    info_rect.bottomleft = (20, WINHEIGHT - 35)
    map_width = len(map_obj) * TILEWIDTH
    map_height = (len(map_obj[0]) - 1) * TILEFLOORHEIGHT + TILEHEIGHT
    max_cam_x_pan = abs(HALF_WINHEIGHT - int(map_height / 2)) + TILEWIDTH
    max_cam_y_pan = abs(HALF_WINWIDTH - int(map_width / 2)) + TILEHEIGHT

    level_is_complete = False
    # Track how much the camera has moved:
    camera_offset_x = 0
    camera_offset_y = 0
    # Track if the keys to move the camera are being held down:
    camera_up = False
    camera_down = False
    camera_left = False
    camera_right = False

    solution = ""
    running = True
    while running:  # main game loop
        # Reset these variables:
        player_move_to = None
        key_pressed = False

        for event in pygame.event.get():  # event handling loop
            if event.type == pygame.QUIT:
                # Player clicked the "X" at the corner of the window.
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                # Handle key presses
                key_pressed = True
                if event.key == pygame.K_LEFT:
                    player_move_to = LEFT
                elif event.key == pygame.K_RIGHT:
                    player_move_to = RIGHT
                elif event.key == pygame.K_UP:
                    player_move_to = UP
                elif event.key == pygame.K_DOWN:
                    player_move_to = DOWN

                # Set the camera move mode.
                elif event.key == pygame.K_a:
                    camera_left = True
                elif event.key == pygame.K_d:
                    camera_right = True
                elif event.key == pygame.K_w:
                    camera_up = True
                elif event.key == pygame.K_s:
                    camera_down = True

                elif event.key == pygame.K_n:
                    return 'next'
                elif event.key == pygame.K_b:
                    return 'back'

                elif event.key == pygame.K_c:
                    solution = solvelevel(level_obj['map_obj'])

                elif event.key == pygame.K_ESCAPE:
                    # running = False # Esc key quits.
                    return 'menu'
                elif event.key == pygame.K_BACKSPACE:
                    return 'reset'  # Reset the level.
                elif event.key == pygame.K_p:
                    # Change the player image to the next one.
                    currentImage += 1
                    if currentImage >= len(PLAYERIMAGES):
                        # After the last player image, use the first one.
                        currentImage = 0
                    map_needs_redraw = True

            elif event.type == pygame.KEYUP:
                # Unset the camera move mode.
                if event.key == pygame.K_a:
                    camera_left = False
                elif event.key == pygame.K_d:
                    camera_right = False
                elif event.key == pygame.K_w:
                    camera_up = False
                elif event.key == pygame.K_s:
                    camera_down = False

        if player_move_to is not None and not level_is_complete:
            # If the player pushed a key to move, make the move
            # (if possible) and push any stars that are pushable.
            moved = makemove(map_obj, game_state_obj, player_move_to)

            if moved:
                # increment the step counter.
                game_state_obj['stepCounter'] += 1
                map_needs_redraw = True

            if is_level_finished(level_obj, game_state_obj):
                # level is solved, we should show the "Solved!" image.
                level_is_complete = True
                key_pressed = False

        DISPLAYSURF.fill(BGCOLOR)

        if map_needs_redraw:
            map_surf = drawmap(map_obj, game_state_obj, level_obj['goals'])
            map_needs_redraw = False

        if camera_up and camera_offset_y < max_cam_x_pan:
            camera_offset_y += CAM_MOVE_SPEED
        elif camera_down and camera_offset_y > -max_cam_x_pan:
            camera_offset_y -= CAM_MOVE_SPEED
        if camera_left and camera_offset_x < max_cam_y_pan:
            camera_offset_x += CAM_MOVE_SPEED
        elif camera_right and camera_offset_x > -max_cam_y_pan:
            camera_offset_x -= CAM_MOVE_SPEED

        # Adjust map_surf's Rect object based on the camera offset.
        map_surf_rect = map_surf.get_rect()
        map_surf_rect.center = (HALF_WINWIDTH + camera_offset_x, HALF_WINHEIGHT + camera_offset_y)

        # Draw map_surf to the DISPLAYSURF Surface object.
        DISPLAYSURF.blit(map_surf, map_surf_rect)

        DISPLAYSURF.blit(level_surf, level_rect)
        DISPLAYSURF.blit(info_surf, info_rect)
        step_surf = BASICFONT.render('Steps: %s. %s' % (game_state_obj['stepCounter'], solution), 1, TEXTCOLOR)
        step_rect = step_surf.get_rect()
        step_rect.bottomleft = (20, WINHEIGHT - 10)
        DISPLAYSURF.blit(step_surf, step_rect)

        if level_is_complete:
            # is solved, show the "Solved!" image until the player
            # has pressed a key.
            solved_rect = IMAGESDICT['solved'].get_rect()
            solved_rect.center = (HALF_WINWIDTH, HALF_WINHEIGHT)
            DISPLAYSURF.blit(IMAGESDICT['solved'], solved_rect)

            if key_pressed:
                return 'solved'

        pygame.display.update()  # draw DISPLAYSURF to the screen.
        FPSCLOCK.tick()


def decoratemap(map_obj, startxy):
    """Makes a copy of the given map object and modifies it.
    Here is what is done to it:
        * Walls that are corners are turned into corner pieces.
        * The outside/inside floor tile distinction is made.
        * Tree/rock decorations are randomly added to the outside tiles.

    Returns the decorated map object."""

    startx, starty = startxy  # Syntactic sugar

    # Copy the map object so we don't modify the original passed
    map_obj_copy = copy.deepcopy(map_obj)

    # Remove the non-wall characters from the map data
    for x in range(len(map_obj_copy)):
        for y in range(len(map_obj_copy[0])):
            if map_obj_copy[x][y] in ('$', '.', '@', '+', '*'):
                map_obj_copy[x][y] = ' '

    # Flood fill to determine inside/outside floor tiles.
    floodfill(map_obj_copy, startx, starty, ' ', 'o')

    # Convert the adjoined walls into corner tiles.
    for x in range(len(map_obj_copy)):
        for y in range(len(map_obj_copy[0])):

            if map_obj_copy[x][y] == '#':
                if (is_wall(map_obj_copy, x, y - 1) and is_wall(map_obj_copy, x + 1, y)) or \
                        (is_wall(map_obj_copy, x + 1, y) and is_wall(map_obj_copy, x, y + 1)) or \
                        (is_wall(map_obj_copy, x, y + 1) and is_wall(map_obj_copy, x - 1, y)) or \
                        (is_wall(map_obj_copy, x - 1, y) and is_wall(map_obj_copy, x, y - 1)):
                    map_obj_copy[x][y] = 'x'

            elif map_obj_copy[x][y] == ' ' and random.randint(0, 99) < OUTSIDE_DECORATION_PCT:
                map_obj_copy[x][y] = random.choice(list(OUTSIDEDECOMAPPING.keys()))

    return map_obj_copy


def is_level_finished(level_obj, game_state_obj):
    """Returns True if all the goals have stars in them."""
    for goal in level_obj['goals']:
        if goal not in game_state_obj['stars']:
            # Found a space with a goal but no star on it.
            return False
    return True


def makemove(map_obj, game_state_obj, player_move_to):
    """Given a map and game state object, see if it is possible for the
    player to make the given move. If it is, then change the player's
    position (and the position of any pushed star). If not, do nothing.

    Returns True if the player moved, otherwise False."""

    # Make sure the player can move in the direction they want.
    playerx, playery = game_state_obj['player']

    # This variable is "syntactic sugar". Typing "stars" is more
    # readable than typing "game_state_obj['stars']" in our code.
    stars = game_state_obj['stars']

    # The code for handling each of the directions is so similar aside
    # from adding or subtracting 1 to the x/y coordinates. We can
    # simplify it by using the x_offset and y_offset variables.
    if player_move_to == UP:
        x_offset = 0
        y_offset = -1
    elif player_move_to == RIGHT:
        x_offset = 1
        y_offset = 0
    elif player_move_to == DOWN:
        x_offset = 0
        y_offset = 1
    elif player_move_to == LEFT:
        x_offset = -1
        y_offset = 0
    else:
        x_offset = 0
        y_offset = 0

    # See if the player can move in that direction.
    if is_wall(map_obj, playerx + x_offset, playery + y_offset):
        return False
    else:
        if (playerx + x_offset, playery + y_offset) in stars:
            # There is a star in the way, see if the player can push it.
            if not isblocked(map_obj, game_state_obj, playerx + (x_offset * 2), playery + (y_offset * 2)):
                # Move the star.
                ind = stars.index((playerx + x_offset, playery + y_offset))
                stars[ind] = (stars[ind][0] + x_offset, stars[ind][1] + y_offset)
            else:
                return False
        # Move the player upwards.
        game_state_obj['player'] = (playerx + x_offset, playery + y_offset)
        return True


def is_wall(map_obj, x, y):
    """Returns True if the (x, y) position on
    the map is a wall, otherwise return False."""
    if x < 0 or x >= len(map_obj) or y < 0 or y >= len(map_obj[x]):
        return False  # x and y aren't actually on the map.
    elif map_obj[x][y] in ('#', 'x'):
        return True  # wall is blocking
    return False


def isblocked(map_obj, game_state_obj, x, y):
    """Returns True if the (x, y) position on the map is
    blocked by a wall or star, otherwise return False."""

    if is_wall(map_obj, x, y):
        return True

    elif x < 0 or x >= len(map_obj) or y < 0 or y >= len(map_obj[x]):
        return True  # x and y aren't actually on the map.

    elif (x, y) in game_state_obj['stars']:
        return True  # a star is blocking

    return False


def floodfill(map_obj, x, y, old_character, new_character):
    """Changes any values matching old_character on the map object to
    new_character at the (x, y) position, and does the same for the
    positions to the left, right, down, and up of (x, y), recursively."""

    # In this game, the flood fill algorithm creates the inside/outside
    # floor distinction. This is a "recursive" function.
    # For more info on the Flood Fill algorithm, see:
    #   http://en.wikipedia.org/wiki/Flood_fill
    if map_obj[x][y] == old_character:
        map_obj[x][y] = new_character

    if x < len(map_obj) - 1 and map_obj[x + 1][y] == old_character:
        floodfill(map_obj, x + 1, y, old_character, new_character)  # call right
    if x > 0 and map_obj[x - 1][y] == old_character:
        floodfill(map_obj, x - 1, y, old_character, new_character)  # call left
    if y < len(map_obj[x]) - 1 and map_obj[x][y + 1] == old_character:
        floodfill(map_obj, x, y + 1, old_character, new_character)  # call down
    if y > 0 and map_obj[x][y - 1] == old_character:
        floodfill(map_obj, x, y - 1, old_character, new_character)  # call up


def printlevel(level):
    fixed_level = ""
    for row in level:
        for char in row:
            # print(char, end="")
            fixed_level += char
        # print()
        fixed_level += "\n"
    return fixed_level


def solvelevel(level):
    # print("mapa nr", levelNum, "\n", str(levelObj['mapObj']), print(printlevel(levelObj['mapObj'])))
    level_to_solve = printlevel(level)
    solved = SolveMap.run(level_to_solve)
    # print(SolveMap.run(level_to_solve))
    print(solved)
    return solved
