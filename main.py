""" pythoban main file. runs main menu.

source code: https://github.com/maliszew/pythoban """
import sys
import pygame
import game
from menuoption import MenuOption


# todo: better intro
HELPTEXT = "Pythoban (Python + Sokoban) game by maliszew.\nTo work, this app needs pygame."
RESOLUTION = 720, 480
FPS = 60

if ("-h" in sys.argv) or ("--help" in sys.argv):
    print(HELPTEXT)
    exit()

print("Nothing much here (yet)!\nRunning Python " + str(sys.version))


def menu():
    pygame.init()
    window = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("Pythoban by maliszew")
    options = [MenuOption("NEW GAME", (140, 105), window),
               MenuOption("LOAD GAME", (140, 155), window),
               MenuOption("OPTIONS", (140, 205), window),
               MenuOption("EXIT", (140, 255), window)]
    clock = pygame.time.Clock()
    # pygame.key.set_repeat(1, 1)

    running = True
    current_option = -1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                pygame.mouse.set_visible(False)
                if event.key == pygame.K_DOWN:
                    if current_option < len(options) - 1:
                        current_option += 1
                    else:
                        current_option = 0
                elif event.key == pygame.K_UP:
                    if current_option > 0:
                        current_option -= 1
                    else:
                        current_option = len(options) - 1
                elif event.key == pygame.K_ESCAPE:
                    print("Pythoban closed. Goodbye!")
                    running = False

                """To prevent too much multiple pressing at once"""
                clock.tick(7)
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                pygame.mouse.set_visible(True)
                current_option = -1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if current_option == 3:
                        print("Pythoban closed. Goodbye!")
                        running = False
                    elif current_option == 0:
                        game.run()
            elif event.type == pygame.MOUSEBUTTONUP:
                for option in options:
                    if option.rect.collidepoint(pygame.mouse.get_pos()):
                        if option.text == "EXIT":
                            print("Pythoban closed. Goodbye!")
                            running = False
                        elif option.text == "NEW GAME":
                            game.run()

        for option in options:
            # todo: prevent option from being hovered when it is selected by mouse, but user is using a keyboard
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
            else:
                option.hovered = False
            option.draw()
        if current_option is not -1:
            options[current_option].hovered = True
            options[current_option].draw()
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    menu()
    pygame.quit()
