import pygame
import math
import os

class Gun(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path_idle = os.path.join(base_dir, 'assets', 'game', 'assets', 'Gun', 'gun.png')
        path_shoot = os.path.join(base_dir, 'assets', 'game', 'assets', 'Gun', 'gun_shoot.png')
        
        self.gun_size = 96
        self.idle_image = pygame.image.load(path_idle).convert_alpha()
        self.idle_image = pygame.transform.scale(self.idle_image, (self.gun_size, self.gun_size))
        
        self.shoot_image = pygame.image.load(path_shoot).convert_alpha()
        self.shoot_image = pygame.transform.scale(self.shoot_image, (self.gun_size, self.gun_size))
        
        self.original_image = self.idle_image
        self.image = self.original_image
        self.rect = self.image.get_rect()
        
        self.is_shooting = False
        self.shoot_duration = 50 
        self.last_shoot_time = 0

    def update(self, camera_x, camera_y):
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            self.is_shooting = True
            self.last_shoot_time = pygame.time.get_ticks()
            self.original_image = self.shoot_image
        else:
            if pygame.time.get_ticks() - self.last_shoot_time > self.shoot_duration:
                self.is_shooting = False
                self.original_image = self.idle_image

        mouse_pos = pygame.mouse.get_pos()
        dx = mouse_pos[0] - (self.player.rect.centerx - camera_x)
        dy = mouse_pos[1] - (self.player.rect.centery - camera_y)
        angle = math.degrees(math.atan2(-dy, dx))

        if dx < 0:
            flipped_image = pygame.transform.flip(self.original_image, False, True)
            self.image = pygame.transform.rotate(flipped_image, angle)
        else:
            self.image = pygame.transform.rotate(self.original_image, angle)
            
        direction_vector = pygame.math.Vector2(1, 0).rotate(-angle)
        offset_dist = 10 
        spawn_pos = pygame.math.Vector2(self.player.rect.center) + direction_vector * offset_dist
        self.rect = self.image.get_rect(center=spawn_pos)

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))