import pygame
import sys
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 48, bold=True)
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path_to_menu_bg = os.path.join(base_dir, 'assets', 'game', 'background', 'mainmenu.png') 
        
        try:
            self.bg_image = pygame.image.load(path_to_menu_bg).convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error:
            self.bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.bg_image.fill((15, 15, 15))
        
        self.color_idle = (200, 200, 200)
        self.color_hover = (255, 0, 0) 
        
        self.start_surf_idle = self.font.render("START", True, self.color_idle)
        self.start_surf_hover = self.font.render("START", True, self.color_hover)
        self.start_rect = self.start_surf_idle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self.exit_surf_idle = self.font.render("EXIT", True, self.color_idle)
        self.exit_surf_hover = self.font.render("EXIT", True, self.color_hover)
        self.exit_rect = self.exit_surf_idle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

    def run(self):
        menu_running = True
        pygame.mouse.set_visible(True)
        while menu_running:
            self.screen.blit(self.bg_image, (0, 0))
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_clicked = True
                        

            if self.start_rect.collidepoint(mouse_pos):
                self.screen.blit(self.start_surf_hover, self.start_rect)
                if mouse_clicked:
                    menu_running = False
                    pygame.mouse.set_visible(False)
            else:
                self.screen.blit(self.start_surf_idle, self.start_rect)
                
            if self.exit_rect.collidepoint(mouse_pos):
                self.screen.blit(self.exit_surf_hover, self.exit_rect)
                if mouse_clicked:
                    pygame.quit()
                    sys.exit()
            else:
                self.screen.blit(self.exit_surf_idle, self.exit_rect)
                
            pygame.display.flip()
            self.clock.tick(FPS)