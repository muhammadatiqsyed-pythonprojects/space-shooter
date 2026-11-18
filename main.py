import asyncio
import random

import pygame

import settings
from bullet import Bullet
from enemy import Enemy
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
    # enemy list
    enemy_list = []
    # enemy creation timer
    enemy_timer = 0

    # player class object
    player = Player()
    # max lives
    lives = settings.MAX_LIVES

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

        # creating and adding bullets to the bullet list initially immediately and then after cooldown time
        shoot_timer -= dt
        if player.wants_to_shoot and shoot_timer <= 0:
            bullet_list.append(Bullet(player.rect.midtop))
            shoot_timer = settings.PLAYER_SHOOT_COOLDOWN
        # handling movement of the bullet
        for bullet in bullet_list:
            bullet.update(dt)

        # bullet removal from the list
        for bullet in bullet_list[:]:
            if bullet.is_off_screen():
                bullet_list.remove(bullet)

        # creating enemies with different center positions and adding them to the enemy list
        enemy_timer -= dt
        if enemy_timer <= 0:
            enemy_pos = (
                random.randint(
                    window_rect.left + settings.ENEMY_WIDTH // 2,
                    window_rect.right - settings.ENEMY_WIDTH // 2,
                ),
                0,
            )
            enemy_list.append(Enemy(enemy_pos))
            enemy_timer = settings.ENEMY_SPAWN_INTERVAL

        # handling enemies movement
        for enemy in enemy_list:
            enemy.update(dt)

        # removing enemies from the enemy list
        for enemy in enemy_list[:]:
            if enemy.is_off_screen():
                enemy_list.remove(enemy)

        # handling enemy and bullet collision
        for enemy in enemy_list[:]:
            for bullet in bullet_list[:]:
                if enemy.rect.colliderect(bullet.rect):
                    enemy_list.remove(enemy)
                    bullet_list.remove(bullet)
                    break

        # handling enemy and player collision
        for enemy in enemy_list[:]:
            if enemy.rect.colliderect(player.rect):
                enemy_list.remove(enemy)
                lives -= 1
                print(lives)

        # --------------------------------DRAW--------------------------------------------
        window.fill(settings.BG_COLOR)

        player.draw(window)

        for bullet in bullet_list:
            bullet.draw(window)

        for enemy in enemy_list:
            enemy.draw(window)

        pygame.display.flip()
        await asyncio.sleep(0)

    # ------------------------------------EXIT--------------------------------------------
    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
