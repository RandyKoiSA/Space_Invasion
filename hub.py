import pygame
from screens.game_screen import GameScreen
from gamemode import GameMode


class Hub:
    """ HUB class, provide a central place to hold all the properties that are constantly being accessed """
    def __init__(self):
        """ Initializing properties """
        self.CLOCK = pygame.time.Clock()
        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 720
        self.BG_COLOR = (125, 125, 125)
        self.main_screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.game_mode = GameMode(self)

        self.shoot_sound = pygame.mixer.Sound('wav/Laser.wav')
        self.enemy_dies_sound = pygame.mixer.Sound('wav/Enemy_Dies.wav')

        self.controller = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }

        self.game_screen = GameScreen(self)

    def displayscreen(self):
        self.game_screen.run()
