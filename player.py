import pygame

import settings


class Player:
    image = None

    def __init__(self):
        if Player.image is None:
            img = pygame.image.load(settings.PLAYER_IMAGE).convert_alpha()
            Player.image = pygame.transform.smoothscale(
                img, (settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT)
            )
        self.rect = pygame.FRect(0, 0, settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT)
        self.rect.center = (settings.PLAYER_START_X, settings.PLAYER_START_Y)
        self.color = settings.PLAYER_COLOR
        self.speed = settings.PLAYER_SPEED
        self.direction = 0
        self.wants_to_shoot = False
        # ignore the pointer until it has been released once, so a tap that
        # started the game or resumed it doesn't immediately steer and fire
        self.pointer_armed = False

    def handle_input(self, pointer_blocked=False):
        self.direction = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction += 1
        self.wants_to_shoot = keys[pygame.K_SPACE]

        # touch or mouse: hold to follow the pointer and fire
        # (pointer_blocked is True while a touch that began on the pause button is held)
        if not pygame.mouse.get_pressed()[0]:
            self.pointer_armed = True
        elif self.pointer_armed and not pointer_blocked:
            target_x = pygame.mouse.get_pos()[0]
            if target_x < self.rect.centerx - settings.TOUCH_DEADZONE:
                self.direction = -1
            elif target_x > self.rect.centerx + settings.TOUCH_DEADZONE:
                self.direction = 1
            self.wants_to_shoot = True

    def update(self, dt, bounds):
        self.rect.centerx += self.speed * dt * self.direction
        self.rect.clamp_ip(bounds)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
