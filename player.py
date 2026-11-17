import pygame

import settings


class Player:
    def __init__(self):
        self.rect = pygame.FRect(0, 0, settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT)
        self.rect.center = (settings.PLAYER_START_X, settings.PLAYER_START_Y)
        self.color = settings.PLAYER_COLOR
        self.speed = settings.PLAYER_SPEED
        self.direction = 0

    def handle_input(self):
        self.direction = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction += 1

    def update(self, dt, bounds):
        self.rect.centerx += self.speed * dt * self.direction
        self.rect.clamp_ip(bounds)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
