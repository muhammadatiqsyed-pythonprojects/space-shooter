import pygame

import settings


class Enemy:
    image = None

    def __init__(self, start_pos, speed):
        if Enemy.image is None:
            img = pygame.image.load(settings.ENEMY_IMAGE).convert_alpha()
            Enemy.image = pygame.transform.smoothscale(
                img, (settings.ENEMY_WIDTH, settings.ENEMY_HEIGHT)
            )
        self.rect = pygame.FRect(0, 0, settings.ENEMY_WIDTH, settings.ENEMY_HEIGHT)
        self.rect.center = start_pos
        self.color = settings.ENEMY_COLOR
        self.speed = speed

    def update(self, dt):
        self.rect.y += self.speed * dt

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def is_off_screen(self):
        return self.rect.top >= settings.WINDOW_HEIGHT
