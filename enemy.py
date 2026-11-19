import pygame

import settings


class Enemy:
    def __init__(self, start_pos, speed):
        self.rect = pygame.FRect(0, 0, settings.ENEMY_WIDTH, settings.ENEMY_HEIGHT)
        self.rect.center = start_pos
        self.color = settings.ENEMY_COLOR
        self.speed = speed

    def update(self, dt):
        self.rect.y += self.speed * dt

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def is_off_screen(self):
        return self.rect.top >= settings.WINDOW_HEIGHT
