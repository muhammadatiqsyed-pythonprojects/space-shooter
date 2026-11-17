import asyncio

import pygame

import settings
from bullet import Bullet
from player import Player


# main function
async def main():
    # ------------------------------SET UP -----------------------------------------
    pygame.init()
    window = pygame.display.set_mode(
        (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT),
        pygame.RESIZABLE | pygame.SCALED,
    )
    pygame.display.set_caption(settings.WINDOW_CAPTION)
    clock = pygame.time.Clock()

    # ---------variables---------
    # loop variable
    running = True
    # window bounds
    window_rect = window.get_rect()
    # bullet list
    bullet_list = []
    # shoot cool down countdown(seconds)
    shoot_timer = 0

    # player class object
    player = Player()

    # game loop
    while running:
        dt = clock.tick(settings.FPS) / 1000
        # ---------------------------------INPUT---------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        player.handle_input()
        # ---------------------------------UPDATE----------------------------------------
        player.update(dt, window_rect)

        shoot_timer -= dt
        if player.wants_to_shoot and shoot_timer <= 0:
            bullet_list.append(Bullet(player.rect.midtop))
            shoot_timer = settings.PLAYER_SHOOT_COOLDOWN

        for bullet in bullet_list:
            bullet.update(dt)

        # bullet removal from the list
        for bullet in bullet_list[:]:
            if bullet.is_off_screen():
                bullet_list.remove(bullet)

        # --------------------------------DRAW--------------------------------------------
        window.fill(settings.BG_COLOR)

        player.draw(window)

        for bullet in bullet_list:
            bullet.draw(window)

        pygame.display.flip()
        await asyncio.sleep(0)

    # ------------------------------------EXIT--------------------------------------------
    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
