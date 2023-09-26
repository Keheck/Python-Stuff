import pygame

def main():
    pygame.init()
    pygame.display.set_caption("Atomas Clone")

    screen = pygame.display.set_mode((720, 540))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


main()
