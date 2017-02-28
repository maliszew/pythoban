"""Game main file. Runs pygame gameboard."""
import pygame

from core import LoadMaps, RunLevel

MAPS_FILE = "starPusherLevels.txt"

RESOLUTION = 1200, 600
FPS = 60
WINWIDTH = 1200  # width of the program's window, in pixels
WINHEIGHT = 600  # height in pixels


def run():
    pygame.init()
    window = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("Pythoban by maliszew")
    fps_clock = pygame.time.Clock()

    # Because the Surface object stored in display_surf was returned
    # from the pygame.display.set_mode() function, this is the
    # Surface object that is drawn to the actual computer screen
    # when pygame.display.update() is called.
    display_surf = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

    pygame.display.set_caption('Pythoban by maliszew!')
    basic_font = pygame.font.Font(None, 40)

    images_dict = {'uncovered goal': pygame.image.load('assets/RedSelector.png'),
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

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Game closed.")
                    running = False
            else:
                maps = LoadMaps.LoadMaps(MAPS_FILE)
                maps.read_file()
                current_level_index = 0

                # The main game loop. This loop runs a single level, when the user
                # finishes that level, the next/previous level is loaded.
                while True:  # main game loop
                    # Run the level to actually start playing the game:
                    result = RunLevel.runlevel(maps.levels, current_level_index)

                    if result in ('solved', 'next'):
                        # Go to the next level.
                        current_level_index += 1
                        if current_level_index >= len(maps.levels):
                            # If there are no more levels, go back to the first one.
                            current_level_index = 0
                    elif result == 'back':
                        # Go to the previous level.
                        current_level_index -= 1
                        if current_level_index < 0:
                            # If there are no previous levels, go to the last one.
                            current_level_index = len(maps.levels) - 1
                    elif result == 'reset':
                        pass  # Do nothing. Loop re-calls runlevel() to reset the level
                    elif result == 'menu':
                        # print("menu")
                        # break
                        running = False

        pygame.display.update()
        fps_clock.tick(FPS)


if __name__ == '__main__':
    run()
    pygame.quit()
