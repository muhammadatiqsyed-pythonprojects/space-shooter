import pygame

import settings


class Bullet:
    def __init__(self, bullet_pos):
        self.rect = pygame.FRect(0, 0, settings.BULLET_WIDTH, settings.BULLET_HEIGHT)
        self.rect.midbottom = bullet_pos
        self.color = settings.BULLET_COLOR
        self.speed = settings.BULLET_SPEED

    def update(self, dt):
        self.rect.y -= self.speed * dt

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def is_off_screen(self):
        return self.rect.bottom <= 0
