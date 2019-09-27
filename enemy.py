import pygame
from pygame.sprite import Sprite


class Enemy(Sprite):
    """ Enemy class, the alien of the game """

    def __init__(self, hub):
        super().__init__()
        self.game_hub = hub
        self.game_mode = self.game_hub.game_mode

        # Load the enemy image
        self.image = pygame.image.load('imgs/Enemies/enemyRed1.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

        self.movingRight = True
        self.velocity = self.game_mode.ship_speed_factor
        self.movingDown = False

    def update(self):
        if self.movingRight:
            self.rect.x += self.velocity
        else:
            self.rect.x -= self.velocity

        self.check_boundaries()

    def draw(self):
        self.game_hub.main_screen.blit(self.image, self.rect)

    def check_boundaries(self):
        if self.rect.left < 0 or self.rect.right > self.game_hub.WINDOW_WIDTH:
            self.movingDown = True
            self.movingRight = not self.movingRight
            self.rect.y += 50
