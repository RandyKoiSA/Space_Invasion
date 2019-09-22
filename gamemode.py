

class GameMode():
    """ Tracks statistics and the win / lose condition """
    def __init__(self, hub):
        """ Initializing default values """
        self.game_hub = hub
        self.player_lives = 3
        self.game_active = False
        self.speedup_scale = 1.1
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.enemy_speed_factor = 1
        self.level = 1
        self.score = 0
        self.enemy_point_value = 50
        self.high_score = 0

    def reset_stats(self):
        self.player_lives = 3
        self.level = 1
        self.score = 0
        self.enemy_point_value = 50

    def increase_speed(self):
        """ Increase speed """
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.enemy_speed_factor *= self.speedup_scale
        self.enemy_point_value += 50
