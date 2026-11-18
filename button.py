import pygame

import settings


class Button:
    def __init__(self, button_pos_y):
        self.rect = pygame.FRect(0, 0, settings.BUTTON_WIDTH, settings.BUTTON_HEIGHT)
        self.rect.center = (settings.WINDOW_WIDTH // 2, button_pos_y)

    def draw_text(self, font, text, color, bg_color, surface):
        pygame.draw.rect(surface, bg_color, self.rect)
        font_img = font.render(text, True, color)
        text_rect = font_img.get_rect(center=self.rect.center)
        surface.blit(font_img, text_rect)
