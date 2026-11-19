import pygame

import settings


class Button:
    def __init__(self, pos_y, font, color, bg_color):
        self.rect = pygame.FRect(0, 0, settings.BUTTON_WIDTH, settings.BUTTON_HEIGHT)
        self.rect.center = (settings.WINDOW_WIDTH // 2, pos_y)
        self.font = font
        self.color = color
        self.bg_color = bg_color

    def draw_text(self, text, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)
        text_img = self.font.render(text, True, self.color)
        text_rect = text_img.get_rect(center=self.rect.center)
        surface.blit(text_img, text_rect)
