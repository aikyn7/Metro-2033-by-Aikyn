import pygame
import math
import os

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, 'assets', 'game', 'assets', 'Gun', 'bullet.png')
        
        self.original_image = pygame.image.load(path).convert_alpha()
        
        self.original_image = pygame.transform.scale(self.original_image, (30, 15))
        
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=pos)
        
        self.speed = 25
        self.angle_rad = math.radians(angle)
        self.vx = math.cos(self.angle_rad) * self.speed
        self.vy = -math.sin(self.angle_rad) * self.speed

    def update(self):

        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.x < -1000 or self.rect.x > 5000 or self.rect.y < -1000 or self.rect.y > 5000:
            self.kill()