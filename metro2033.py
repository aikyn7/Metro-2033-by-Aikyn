import pygame
import sys
import os

from player import Player
from settings import *


def main():

    pygame.init()

    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    pygame.display.set_caption(
        "Metro 2033"
    )

    clock = pygame.time.Clock()

    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

    path_to_bg = os.path.join(
        BASE_DIR,
        'assets',
        'game',
        'background',
        'background.png'
    )

    path_to_player = os.path.join(
        BASE_DIR,
        'assets',
        'game',
        'assets',
        'Player',
        'PlayerBase.png'
    )

    bg_image = pygame.image.load(
        path_to_bg
    ).convert()

    bg_image = pygame.transform.scale(
        bg_image,
        (
            bg_image.get_width() * 2,
            bg_image.get_height() * 2
        )
    )

    map_width = bg_image.get_width()
    map_height = bg_image.get_height()

    walls = []

    TILE = 128

    def add_wall_tile(col, row):

        walls.append(
            pygame.Rect(
                col * TILE,
                row * TILE,
                TILE,
                TILE
            )
        )

    #collison
    for col in range(0, 24):
        add_wall_tile(col, 4)

    for row in range(4, 12):
        for col in range(0, 3):
            add_wall_tile(col, row)

    for row in range(6, 16):
        add_wall_tile(11, row)
        add_wall_tile(12, row)

    for row in range(3, 16):
        for col in range(19, 24):
            add_wall_tile(col, row)
            
    for col in range(19, 24):
        add_wall_tile(col, 2)
    for col in range(0, 24):
        add_wall_tile(col, 15)
    
    add_wall_tile(3,6)
    add_wall_tile(4,6)
    add_wall_tile(5,6)
    add_wall_tile(5,7)
    add_wall_tile(5,8)

    
    
    
    
    
    #player
    player = Player(
        path_to_player,
        16,
        16,
        walls,
        map_width,
        map_height
    )

    all_sprites = pygame.sprite.Group()

    all_sprites.add(player)

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()

        camera_x = int(
            player.rect.centerx
            - SCREEN_WIDTH // 2
        )

        camera_y = int(
            player.rect.centery
            - SCREEN_HEIGHT // 2
        )

        camera_x = max(
            0,
            min(
                camera_x,
                map_width - SCREEN_WIDTH
            )
        )

        camera_y = max(
            0,
            min(
                camera_y,
                map_height - SCREEN_HEIGHT
            )
        )

        screen.blit(
            bg_image,
            (-camera_x, -camera_y)
        )

        for sprite in all_sprites:

            screen.blit(
                sprite.image,
                (
                    sprite.rect.x - camera_x,
                    sprite.rect.y - camera_y
                )
            )

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()

    sys.exit()


if __name__ == "__main__":
    main()