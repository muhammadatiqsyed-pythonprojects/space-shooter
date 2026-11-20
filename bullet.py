import pygame

import settings


class Bullet:
    image = None

    def __init__(self, bullet_pos):
        if Bullet.image is None:
            img = pygame.image.load(settings.BULLET_IMAGE).convert_alpha()
            Bullet.image = pygame.transform.smoothscale(
                img, (settings.BULLET_WIDTH, settings.BULLET_HEIGHT)
            )
        self.rect = pygame.FRect(0, 0, settings.BULLET_WIDTH, settings.BULLET_HEIGHT)
        self.rect.midbottom = bullet_pos
        self.color = settings.BULLET_COLOR
        self.speed = settings.BULLET_SPEED

    def update(self, dt):
        self.rect.y -= self.speed * dt

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def is_off_screen(self):
        return self.rect.bottom <= 0
