import pygame
import os

class Crosshair:
    def __init__(self, base_dir):
        # Прячем стандартный курсор Windows
        pygame.mouse.set_visible(False)
        
        # Собираем путь к картинке прицела
        path = os.path.join(base_dir, 'assets', 'game', 'assets', 'gun', 'crosshair.png')
        
        try:
            original_image = pygame.image.load(path).convert_alpha()
            
            # --- ИЗМЕНЕНИЕ РАЗМЕРА КУРСОРA ---
            # Задай здесь нужный размер. Например, (32, 32) вместо исходных 64х64
            new_size = (32, 32) 
            self.image = pygame.transform.scale(original_image, new_size)
            # ---------------------------------
            
        except pygame.error:
            # Если арт потерялся, создаем аккуратный красный квадрат 10х10
            self.image = pygame.Surface((10, 10))
            self.image.fill((255, 0, 0))
            
        # Магия автоматического центрирования:
        # Теперь не важно, какой размер ты укажешь в new_size, 
        # смещение под курсор мыши пересчитается само!
        self.offset_x = self.image.get_width() // 2
        self.offset_y = self.image.get_height() // 2

    def draw(self, screen):
        # Получаем координаты мышки в текущем кадре
        mx, my = pygame.mouse.get_pos()
        # Рисуем прицел ровно по центру курсора
        screen.blit(self.image, (mx - self.offset_x, my - self.offset_y))