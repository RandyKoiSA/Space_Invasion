import pygame
import sys
from pygame.locals import *
from pygame.sprite import Group
from bullet import Bullet
from ship import Ship
from enemy import Enemy
from time import sleep
from button import Button
from score_board import ScoreBoard


class GameScreen:
    """ Game screen, were the game starts """
    def __init__(self, hub):
        """ Initializing default values """
        self.game_hub = hub

        # Initialize player ship: This will be remove as we will loading in levels soon
        self.player_ship = Ship(self.game_hub)

        # Create a group for bullets
        self.bullets = Group()
        # Create a group for enemies
        self.enemies = Group()

        self.enemy = Enemy(self.game_hub)

        self.available_space_x = self.game_hub.WINDOW_WIDTH - 2 * self.enemy.rect.width
        self.number_enemies_x = int(self.available_space_x / (2 * self.enemy.rect.width))
        self.number_of_rows = 3

        # Create play button
        self.play_button = Button(self.game_hub, "Play")

        # Create score board
        self.sb = ScoreBoard(self.game_hub)


    def run(self):
        self.run_event()
        if not self.game_hub.game_mode.game_active:
            self.play_button.draw()
        else:
            self.run_update()
            self.run_draw()

    def run_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_a:
                    self.game_hub.controller['left'] = True
                    self.game_hub.controller['right'] = False
                if event.key == K_d:
                    self.game_hub.controller['right'] = True
                    self.game_hub.controller['left'] = False
                if event.key == K_SPACE:
                    self.add_bullet()
                if event.key == K_t:
                    self.create_fleet()

            if event.type == KEYUP:
                if event.key == K_a:
                    self.game_hub.controller['left'] = False
                if event.key == K_d:
                    self.game_hub.controller['right'] = False

            if event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.check_play_button(mouse_x, mouse_y)

    def run_update(self):
        self.player_ship.update()
        self.update_bullets()
        self.update_enemies()
        self.update_collision()

    def run_draw(self):
        self.player_ship.draw()
        self.sb.draw()
        self.draw_bullets()
        self.draw_enemies()

    def add_bullet(self):
        new_bullet = Bullet(self.game_hub, self.player_ship)
        self.bullets.add(new_bullet)

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.update()

            if bullet.rect.top < 0:
                self.bullets.remove(bullet)

    def draw_bullets(self):
        for bullet in self.bullets:
            bullet.draw()

    def create_fleet(self):
        for enemy_number in range(self.number_enemies_x):
            for number_row in range(self.number_of_rows):
                # Create an alien and place it in the row
                new_enemy = Enemy(self.game_hub)
                new_enemy.rect.x = self.enemy.rect.width + 2 * self.enemy.rect.width * enemy_number
                new_enemy.rect.y = self.enemy.rect.height + 2 * self.enemy.rect.height * number_row
                self.enemies.add(new_enemy)

    def update_enemies(self):
        for enemy in self.enemies:
            enemy.update()

            if enemy.rect.top > self.game_hub.WINDOW_HEIGHT:
                self.enemies.remove(enemy)
                print(len(self.enemies))
            if pygame.sprite.spritecollideany(self.player_ship, self.enemies):
                self.ship_hit()

    def draw_enemies(self):
        for enemy in self.enemies:
            enemy.draw()

    def update_collision(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        if len(self.enemies) <= 0:
            self.bullets.empty()
            self.game_hub.game_mode.increase_speed()
            self.create_fleet()
            self.game_hub.game_mode.level += 1
            self.sb.prep_level()
        if collisions:
            for enemies in collisions.values():
                self.game_hub.game_mode.score += self.game_hub.game_mode.enemy_point_value * len(enemies)
                self.sb.prep_score()
            self.check_high_score()

    def ship_hit(self):
        """ Respond to ship being hit by aliens"""
        # Degrement ships left
        self.game_hub.game_mode.player_lives -= 1

        # Update scoreboard
        self.sb.prep_ships()

        # Empty the list of aliens and bullets
        self.enemies.empty()
        self.bullets.empty()

        # Check if there is any lives left
        if self.game_hub.game_mode.player_lives > 0:
            # Create new fleet
            self.create_fleet()
        if self.game_hub.game_mode.player_lives <= 0:
            self.game_hub.game_mode.game_active = False
            pygame.mouse.set_visible(True)
        # Pause
        sleep(0.5)

    def check_play_button(self, mouse_x, mouse_y):
        if self.play_button.rect.collidepoint(mouse_x, mouse_y):
            self.game_hub.game_mode.game_active = True
            self.game_hub.game_mode.reset_stats()
            self.sb.prep_score()
            self.sb.prep_highscore()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.create_fleet()
            pygame.mouse.set_visible(False)

    def check_high_score(self):
        """ Check to see if there's a new high score. """
        if self.game_hub.game_mode.score > self.game_hub.game_mode.high_score:
            self.game_hub.game_mode.high_score = self.game_hub.game_mode.score
            self.sb.prep_highscore()
