from pathlib import Path

class Settings:
    def __init__(self):
        self.name: str = 'Alien Invasion'
        self.screen_w = 1200
        self.screen_h = 800
        self.FPS = 60
        self.bg_file = Path.cwd() / 'Assets' / 'images' / 'StarBackground.png'
        
        self.ship_file = Path.cwd() / 'Assets' / 'images' / 'TieFighter.png'
        self.ship_w = 80
        self.ship_h = 60
        self.ship_speed = 5

        self.bullet_file = Path.cwd() / 'Assets' / 'images' / 'greenLaserBlast.png'
        self.laser_sound = Path.cwd() / 'Assets' / 'sound' / 'laser2.mp3'
        self.bullet_speed = 7
        self.bullet_w = 25
        self.bullet_h = 80
        self.bullet_amount = 5

        self.alien_file = Path.cwd() / 'Assets' / 'images' / 'xwing.png'
        self.alien_w = 60
        self.alien_h = 60
        self.fleet_speed = 5
        self.fleet_direction = 1

        
