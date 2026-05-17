import pygame
import sys
import os
import random 

from player import Player
from settings import *
from enemy import Enemy
from gun import Gun
from bullet import Bullet
from mainmenu import MainMenu
from crosshair import Crosshair


def main():
    pygame.init()
    
    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )


    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    pygame.display.set_caption(
        "Metro 2033"
    )
    pygame.mouse.set_visible(False)

    crosshair = Crosshair(BASE_DIR)

    menu = MainMenu(screen)
    menu.run()

    clock = pygame.time.Clock()

    score = 0
    max_score = 0
    game_over = False

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

    # 3 sec
    SPAWN_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_ENEMY, 3000)
    current_spawn_delay = 3000

    #player
    player = Player(
        path_to_player,
        16,
        16,
        walls,
        map_width,
        map_height
    )
    #gun
    gun = Gun(player)

    all_sprites = pygame.sprite.Group()
    enemies_group = pygame.sprite.Group()
    all_sprites.add(player)
    score = 0

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == SPAWN_ENEMY:
                spawn_x = random.randint(0, map_width)
                new_zombie = Enemy((spawn_x, 2000), walls, player)
                all_sprites.add(new_zombie)
                enemies_group.add(new_zombie)

        all_sprites.update()
        for sprite in all_sprites:
            if isinstance(sprite, Bullet):
                hit_enemies = pygame.sprite.spritecollide(sprite, enemies_group, False)
                
                if hit_enemies:
                    sprite.kill()
                    
                    for enemy in hit_enemies:
                        enemy.health -= 10 
                        
                        if enemy.health <= 0:
                            enemy.kill() 
                            score += 1
                            new_delay = max(600, 3000 - (score * 100))
                            if new_delay != current_spawn_delay:
                                current_spawn_delay = new_delay
                                pygame.time.set_timer(SPAWN_ENEMY, current_spawn_delay)
        
        camera_x = int(player.rect.centerx - SCREEN_WIDTH // 2)
        camera_y = int(player.rect.centery - SCREEN_HEIGHT // 2)
        camera_x = max(0, min(camera_x, map_width - SCREEN_WIDTH))
        camera_y = max(0, min(camera_y, map_height - SCREEN_HEIGHT))

        new_bullets = gun.update(camera_x, camera_y)
        if new_bullets:
            for bullet in new_bullets:
                all_sprites.add(bullet)

        screen.blit(bg_image, (-camera_x, -camera_y))


        for sprite in all_sprites:
            screen.blit(
                sprite.image,
                (sprite.rect.x - camera_x, sprite.rect.y - camera_y)
            )

        gun.draw(screen, camera_x, camera_y)
        hp_bar_x = 20
        hp_bar_y = screen.get_height() - 110
        hp_bar_width = 200
        hp_bar_height = 25

        pygame.draw.rect(screen, (50, 0, 0), (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height))

        health_ratio = player.health / player.max_health
        current_bar_width = int(hp_bar_width * health_ratio)

        bar_color = (0, 255, 0) if player.health > 30 else (255, 0, 0)
        if player.health <= 0:
            if not game_over: 
                game_over = True
                pygame.mouse.set_visible(True)  
                if score > max_score:
                    max_score = score #система макс очков

        pygame.draw.rect(screen, bar_color, (hp_bar_x, hp_bar_y, current_bar_width, hp_bar_height))

        pygame.draw.rect(screen, (255, 255, 255), (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height), 2)

        gun.draw_ui(screen)
        crosshair.draw(screen)
        score_surface = gun.font.render(f"SCORE: {score}", True, (255, 255, 255))
        screen.blit(score_surface, (SCREEN_WIDTH - score_surface.get_width() - 20, 20))
        #геймовер
        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((15, 15, 15))
            screen.blit(overlay, (0, 0))
            
            go_font = pygame.font.SysFont("Arial", 64, bold=True)
            info_font = pygame.font.SysFont("Arial", 36, bold=True)
            btn_font = pygame.font.SysFont("Arial", 42, bold=True)
            
            color_idle = (200, 200, 200)
            color_hover = (255, 0, 0)
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()[0] 
            
            go_surf = go_font.render("GAME OVER", True, (255, 0, 0))
            score_surf = info_font.render(f"SCORE: {score}", True, (255, 255, 255))
            max_surf = info_font.render(f"MAXIMUM SCORE: {max_score}", True, (255, 215, 0)) # Золотой цвет для рекорда
            
            go_rect = go_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 140))
            score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
            max_rect = max_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10))
            
            screen.blit(go_surf, go_rect)
            screen.blit(score_surf, score_rect)
            screen.blit(max_surf, max_rect)
            
            # 4. СОЗДАЕМ КНОПКУ RESTART
            rest_rect = pygame.Rect(0, 0, 200, 50)
            rest_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)
            
            if rest_rect.collidepoint(mouse_pos):
                rest_surf = btn_font.render("RESTART", True, color_hover)
                if mouse_clicked:
                    #логика сброса
                    score = 0
                    game_over = False
                    player.health = 100
                    player.rect.x = 500
                    player.rect.y = 500
                    player.rect.center = (player.rect.x, player.rect.y)
                    
                    enemies_group.empty()
                    all_sprites.empty() 
                    all_sprites.add(player) 
                    
                    pygame.time.set_timer(SPAWN_ENEMY, 3000)
                    pygame.mouse.set_visible(False)
            else:
                rest_surf = btn_font.render("RESTART", True, color_idle)
                
            screen.blit(rest_surf, rest_surf.get_rect(center=rest_rect.center))
            
            menu_rect = pygame.Rect(0, 0, 200, 50)
            menu_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 140)
            
            if menu_rect.collidepoint(mouse_pos):
                menu_btn_surf = btn_font.render("MENU", True, color_hover)
                if mouse_clicked:
                    menu.run()
                    
                    #сброс в меню
                    score = 0
                    game_over = False
                    player.health = 100
                    player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                    
                    enemies_group.empty()
                    all_sprites.empty()
                    all_sprites.add(player)
                    
                    pygame.time.set_timer(SPAWN_ENEMY, 3000)
                    pygame.mouse.set_visible(False)
            else:
                menu_btn_surf = btn_font.render("MENU", True, color_idle)
                
            screen.blit(menu_btn_surf, menu_btn_surf.get_rect(center=menu_rect.center))
        
        pygame.display.flip()
        
        clock.tick(FPS)
    pygame.quit()

    sys.exit()


if __name__ == "__main__":
    main()