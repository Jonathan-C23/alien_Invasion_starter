from pathlib import Path

class Settings:
    def __init__(self):
        self.name: str = 'Alien Invasion'
        self.screen_w = 1000
        self.screen_h = 800
        self.FPS = 60
        self.bg_file = Path.cwd() / 'Assets' / 'images' / 'StarBackground.png'
        self.difficulty_scale = 1.1
        self.scores_file = Path.cwd() / 'Assets' / 'file' / 'scores.json'
        
        self.ship_file = Path.cwd() / 'Assets' / 'images' / 'TieFighter.png'
        self.ship_w = 80
        self.ship_h = 60

        self.bullet_file = Path.cwd() / 'Assets' / 'images' / 'greenLaserBlast.png'
        self.laser_sound = Path.cwd() / 'Assets' / 'sound' / 'laser2.mp3'
        self.impact_sound = Path.cwd() / 'Assets' / 'sound' / 'impactSound2.mp3'

        self.alien_file = Path.cwd() / 'Assets' / 'images' / 'xwing.png'
        self.alien_w = 50
        self.alien_h = 50
        self.fleet_direction = 1

        self.button_w = 200
        self.button_h = 50
        self.button_color = (0,135,50)
        
        self.text_color = (255, 255, 255)
        self.button_font_size = 48
        self.HUD_font_size = 20
        self.font_file = Path.cwd() / 'Assets' / 'Fonts' / 'Starjedi' / 'Starjedi.ttf'

        self.life_image = Path.cwd() / 'Assets' / 'images' / 'life.png'
        self.life_w = 40
        self.life_h = 40

        self.music = Path.cwd() / 'Assets' / 'sound' / 'music.mp3'

    def initialize_dynamic_settings(self):
        self.ship_speed = 5
        self.starting_ship_count = 2

        self.bullet_speed = 7
        self.bullet_w = 25
        self.bullet_h = 80
        self.bullet_amount = 5

        self.fleet_speed = 4
        self.fleet_drop_speed = 50
        self.alien_points = 50

    def increase_difficulty(self):
        self.ship_speed *= self.difficulty_scale
        self.bullet_speed *= self.difficulty_scale
        self.fleet_speed *= self.difficulty_scale