import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

class Boid(pygame.sprite.Sprite):
    angle: int = 1
    base_image: pygame.Surface = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.base_image = pygame.Surface((32, 32))
        # self.base_image.fill("white")
        # for x in range(32):
        #     for y in range(32):
        #         pygame.draw.rect(self.base_image, (x / 32 * 255, y / 32 * 255, 0), ((x, y), (1, 1)))
        pygame.draw.circle(self.base_image, "white", (16, 16), 16)

        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 500

    def update(self):
        #print(self.angle)
        self.image = pygame.transform.rotate(self.base_image, self.angle)
        self.angle = (self.angle + 1) % 360
        pass
    
boid = Boid()

boid_group = pygame.sprite.Group()
boid_group.add(boid)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    boid_group.update()
    boid_group.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()