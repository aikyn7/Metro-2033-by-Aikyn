import pygame
import os

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, walls, player):
        super().__init__()
        
        self.player = player
        self.walls = walls
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, 'assets', 'game', 'assets', 'Enemy', 'zombie.png')
        
        self.sheet = pygame.image.load(path).convert_alpha()
        
        self.frame_w = 16
        self.frame_h = 16
        self.scale = 4
        
        self.animations = {
            'idle_left': self.get_row(0, 4),
            'idle_right': self.get_row(1, 4),
            'idle_up': self.get_row(2, 4),
            'idle_down': self.get_row(3, 4),
            'walk_left': self.get_row(4, 4),
            'walk_right': self.get_row(5, 4),
            'walk_up': self.get_row(6, 4),
            'walk_down': self.get_row(7, 4)
        }
        
        self.status = 'idle_down'
        self.facing = 'down'
        self.frame_index = 0
        self.animation_speed = 0.12
        
        self.image = self.animations[self.status][0]
        self.rect = self.image.get_rect(center=pos)
        
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.speed = 3

    def get_row(self, row_index, count):
        frames = []
        for i in range(count):
            rect = pygame.Rect(i * self.frame_w, row_index * self.frame_h, self.frame_w, self.frame_h)
            frame = self.sheet.subsurface(rect).copy()
            frame = pygame.transform.scale(frame, (self.frame_w * self.scale, self.frame_h * self.scale))
            frames.append(frame)
        return frames

    def get_direction(self):
        player_vector = pygame.math.Vector2(self.player.rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        
        heading = player_vector - enemy_vector
        
        if heading.length() > 0:
            self.direction = heading.normalize()
        else:
            self.direction = pygame.math.Vector2(0, 0)

    def update_status(self):
        if self.direction.magnitude() == 0:
            self.status = 'idle_' + self.facing
        else:
            if abs(self.direction.x) > abs(self.direction.y):
                self.facing = 'right' if self.direction.x > 0 else 'left'
            else:
                self.facing = 'down' if self.direction.y > 0 else 'up'
            self.status = 'walk_' + self.facing

    def collision(self, direction):
        for wall in self.walls:
            if wall.y == 15 * 128:
                continue
                
            if self.rect.colliderect(wall):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.rect.right = wall.left
                    if self.direction.x < 0: self.rect.left = wall.right
                    self.pos.x = self.rect.centerx
                if direction == 'vertical':
                    if self.direction.y > 0: self.rect.bottom = wall.top
                    if self.direction.y < 0: self.rect.top = wall.bottom
                    self.pos.y = self.rect.centery

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * self.speed
        self.rect.centerx = round(self.pos.x)
        self.collision('horizontal')

        self.pos.y += self.direction.y * self.speed
        self.rect.centery = round(self.pos.y)
        self.collision('vertical')

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]

    def update(self):
        self.get_direction()
        self.update_status()
        self.move()
        self.animate()
        now = pygame.time.get_ticks()
        
        # Создаем векторы позиций игрока и зомби
        player_pos = pygame.math.Vector2(self.player.rect.center)
        enemy_pos = pygame.math.Vector2(self.rect.center)
        
        # Считаем чистое расстояние в пикселях между ними
        distance = player_pos.distance_to(enemy_pos)
        
        # Если зомби подошел ближе чем на 60 пикселей (настрой радиус под себя)
        if distance <= 60:
            # Чтобы хп не улетало за 1 секунду, делаем задержку ударов (кулдаун)
            # Например, зомби бьет раз в 500 миллисекунд (полсекунды)
            if not hasattr(self, 'last_attack_time'):
                self.last_attack_time = 0
                
            if now - self.last_attack_time > 500: 
                self.player.health -= 10 # Отнимаем 10 ХП
                self.last_attack_time = now
                
                # Проверка на смерть игрока
                if self.player.health < 0:
                    self.player.health = 0
        