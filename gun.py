import pygame
import math
import os

from bullet import Bullet

class Gun(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path_idle = os.path.join(base_dir, 'assets', 'game', 'assets', 'Gun', 'gun.png')
        path_shoot = os.path.join(base_dir, 'assets', 'game', 'assets', 'Gun', 'gun_shoot.png')
        path_ammo_icon = os.path.join(base_dir, 'assets', 'game', 'assets', 'Gun', 'ammo_box.png')
        
        self.gun_size = 96
        self.idle_image = pygame.image.load(path_idle).convert_alpha()
        self.idle_image = pygame.transform.scale(self.idle_image, (self.gun_size, self.gun_size))
        
        self.shoot_image = pygame.image.load(path_shoot).convert_alpha()
        self.shoot_image = pygame.transform.scale(self.shoot_image, (self.gun_size, self.gun_size))
        
        self.ammo_icon = pygame.image.load(path_ammo_icon).convert_alpha()
        self.ammo_icon = pygame.transform.scale(self.ammo_icon, (40, 40))
        
        self.original_image = self.idle_image
        self.image = self.original_image
        self.rect = self.image.get_rect()
        
        self.is_shooting = False
        self.shoot_duration = 50 
        self.last_shoot_time = 0

        self.max_ammo = 30
        self.current_ammo = 30
        self.is_reloading = False
        self.reload_time = 3000 
        self.reload_start_time = 0
        self.shoot_cooldown = 0
        self.font = pygame.font.SysFont("Arial", 32, bold=True)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path_to_shoot = os.path.join(base_dir, 'assets', 'game', 'sound', 'ak_shoot.mp3')

        try:
            self.shoot_sound = pygame.mixer.Sound(path_to_shoot)
            self.shoot_sound.set_volume(0.5)
        except pygame.error as e:
            print(f"no shoot {e}")
            self.shoot_sound = None

        self.gun_channel = pygame.mixer.Channel(1)

    def reload(self):
        if not self.is_reloading and self.current_ammo < self.max_ammo:
            self.is_reloading = True
            self.reload_start_time = pygame.time.get_ticks()

    def update(self, camera_x, camera_y):
        bullets = []
        now = pygame.time.get_ticks()

        if self.is_reloading:
            if now - self.reload_start_time >= self.reload_time:
                self.current_ammo = self.max_ammo
                self.is_reloading = False

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        
        dx = mouse_pos[0] - (self.player.rect.centerx - camera_x)
        dy = mouse_pos[1] - (self.player.rect.centery - camera_y)
        angle = math.degrees(math.atan2(-dy, dx))

        if mouse_buttons[0] and self.current_ammo > 0 and not self.is_reloading:
            if self.shoot_cooldown == 0:
                self.is_shooting = True
                self.current_ammo -= 1
                self.last_shoot_time = now
                self.shoot_cooldown = 10 
                self.original_image = self.shoot_image
                
                direction = pygame.math.Vector2(1, 0).rotate(-angle)
                bullet_pos = pygame.math.Vector2(self.player.rect.center) + direction * 45
                bullets.append(Bullet(bullet_pos, angle))
                if self.shoot_sound:
                # play() запускает звук в отдельном канале, 
                # поэтому клики могут накладываться друг на друга, создавая эффект очереди!
                    self.shoot_sound.play()
        
        if now - self.last_shoot_time > self.shoot_duration:
            self.is_shooting = False
            self.original_image = self.idle_image

        if self.current_ammo <= 0:
            self.reload()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]: self.reload()

        if dx < 0:
            flipped_image = pygame.transform.flip(self.original_image, False, True)
            self.image = pygame.transform.rotate(flipped_image, angle)
        else:
            self.image = pygame.transform.rotate(self.original_image, angle)
            
        direction_vector = pygame.math.Vector2(1, 0).rotate(-angle)
        offset_dist = 10 
        spawn_pos = pygame.math.Vector2(self.player.rect.center) + direction_vector * offset_dist
        self.rect = self.image.get_rect(center=spawn_pos)

        return bullets
    
    def draw_ui(self, screen):
        screen.blit(self.ammo_icon, (20, screen.get_height() - 60))
        ammo_text = f"{self.current_ammo} / {self.max_ammo}"
        if self.is_reloading:
            ammo_text = "RELOADING..."
        text_surface = self.font.render(ammo_text, True, (255, 255, 255))
        screen.blit(text_surface, (70, screen.get_height() - 55))

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))