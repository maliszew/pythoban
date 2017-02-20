"""Game main file. Runs pygame gameboard."""
import pygame


RESOLUTION = 720, 480
FPS = 60

def run():
    pygame.init()
    window = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("Pythoban by maliszew")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Game closed.")
                    running = False
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    run()
    pygame.quit()
