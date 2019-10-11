class Settings:
    # A class to store all settings for Alien Invations

    def __init__(self):
        """Initialize the game's static settings"""

        # screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.bgcolor = (0, 0, 0)

        # Bullet settings
        self.bullet_speed_factor = 3
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 0, 250, 30
        self.aibullet_color = 60, 0, 0
        self.WHITE = 255, 255, 255
        self.bullets_allowed = 5

        # ship settings
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # Alien settings
        self.alien_speed_factor = 30
        self.fleet_drop_speed = 10
        self.alien_points = 10
        self.fleet_direction = 1
        self.ai_max_lasers = 5
        self.ai_shoot_chance = 20
        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quicly the alien point values increase
        self.score_scale = 1.5
        self.highscores = ()
        self.listscore = []
        self.initialize_dynamic_settings()
        f = open("highscore.txt", "r")
        if f.mode == "r":
            self.highscores = f.readline()
        f.close()

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.ai_max_lasers += 3
        self.bullets_allowed += 5
        self.ai_shoot_chance *= self.score_scale
        self.alien_points = int(self.alien_points * self.score_scale)

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        # Fleet_direction of 1 is Right; -1 is left
        self.fleet_direction = 1
        # Scoring
        self.alien_points = 50
        # AI shooting
        self.ai_max_lasers = 5
        self.ai_shoot_chance = 20
