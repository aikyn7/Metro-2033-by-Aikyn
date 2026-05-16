import pygame
import os

from settings import *

class Player(pygame.sprite.Sprite):

    def __init__(self, sheet_path, width, height, walls, map_width, map_height):
        super().__init__()
        

        self.max_health = 100
        self.health = 100

        super().__init__()

        self.body_sheet = pygame.image.load(
            sheet_path
        ).convert_alpha()

        self.frame_w = width
        self.frame_h = height
        self.scale = 4

        self.walls = walls
        self.map_width = map_width
        self.map_height = map_height

        self.animations = {
            'idle_left': self.get_row(self.body_sheet, 0, 2),
            'idle_right': self.get_row(self.body_sheet, 1, 2),
            'idle_up': self.get_row(self.body_sheet, 2, 2),
            'idle_down': self.get_row(self.body_sheet, 3, 2),
            'walk_left': self.get_row(self.body_sheet, 4, 2),
            'walk_right': self.get_row(self.body_sheet, 5, 2),
            'walk_up': self.get_row(self.body_sheet, 6, 2),
            'walk_down': self.get_row(self.body_sheet, 7, 2)
        }

        self.status = 'idle_down'
        self.facing = 'down'
        self.frame_index = 0
        self.animation_speed = 0.12

        self.image = self.animations[self.status][0]

        self.rect = self.image.get_rect(
            center=(1500, 700)
        )

        self.pos = pygame.math.Vector2(
            self.rect.center
        )

        self.direction = pygame.math.Vector2()
        self.speed = 7

    def get_row(self, sheet, row_index, count):

        frames = []

        for i in range(count):
            rect = pygame.Rect(
                i * self.frame_w,
                row_index * self.frame_h,
                self.frame_w,
                self.frame_h
            )

            frame = sheet.subsurface(rect).copy()

            frame = pygame.transform.scale(
                frame,
                (
                    self.frame_w * self.scale,
                    self.frame_h * self.scale
                )
            )
            frames.append(frame)

        return frames

    def get_input(self):

        keys = pygame.key.get_pressed()

        self.direction.x = 0
        self.direction.y = 0

        if keys[pygame.K_w]:
            self.direction.y = -1
            self.facing = 'up'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.facing = 'down'

        if keys[pygame.K_a]:
            self.direction.x = -1
            self.facing = 'left'
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.facing = 'right'

    def update_status(self):

        if self.direction.magnitude() == 0:
            self.status = 'idle_' + self.facing
        else:
            self.status = 'walk_' + self.facing

    def collision(self, direction):

        for wall in self.walls:
            if self.rect.colliderect(wall):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.rect.right = wall.left
                    if self.direction.x < 0:
                        self.rect.left = wall.right
                    self.pos.x = self.rect.centerx

                if direction == 'vertical':
                    if self.direction.y > 0:
                        self.rect.bottom = wall.top
                    if self.direction.y < 0:
                        self.rect.top = wall.bottom
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

        self.pos = pygame.math.Vector2(self.rect.center)

    def animate(self):

        animation = self.animations[self.status]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]

    def update(self):
        self.get_input()
        self.update_status()
        self.move()
        self.animate()