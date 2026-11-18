import asyncio
import random

import pygame

import settings
from bullet import Bullet
from button import Button
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
    # font
    game_font = pygame.font.Font(None, 40)
    # Button class objects
    title_button = Button(settings.WINDOW_HEIGHT - 500)
    play_button = Button(settings.WINDOW_HEIGHT - 400)
    score_button = Button(settings.WINDOW_HEIGHT - 300)

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
    # game states
    game_state = "menu"  # other states are playing and gameover
    # keeping the score
    score = 0

    # game loop
    while running:
        dt = clock.tick(settings.FPS) / 1000
        # ---------------------------------INPUT---------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_state in ("menu", "gameover") and (
                (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and play_button.rect.collidepoint(event.pos)
                )
                or (event.type == pygame.KEYDOWN and event.key == pygame.K_p)
            ):
                score = 0
                lives = settings.MAX_LIVES
                shoot_timer = 0
                enemy_timer = 0
                bullet_list = []
                enemy_list = []
                player = Player()
                game_state = "playing"

        if game_state == "playing":
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
                        window_rect.left + settings.ENEMY_SPAWN_MARGIN,
                        window_rect.right - settings.ENEMY_SPAWN_MARGIN,
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
                        score += 1
                        break

            # handling enemy and player collision
            for enemy in enemy_list[:]:
                if enemy.rect.colliderect(player.rect):
                    enemy_list.remove(enemy)
                    lives -= 1

            # game over check
            if lives <= 0:
                game_state = "gameover"

        # --------------------------------DRAW--------------------------------------------
        window.fill(settings.BG_COLOR)

        if game_state == "menu":
            title_button.draw_text(
                game_font, "Welcome Space Shooter!", "white", "darkblue", window
            )
            play_button.draw_text(
                game_font, "Click or press P to Play!", "white", "darkblue", window
            )
        elif game_state == "playing":
            player.draw(window)

            for bullet in bullet_list:
                bullet.draw(window)

            for enemy in enemy_list:
                enemy.draw(window)

            # HUD: score at the top left, lives at the top right
            score_img = game_font.render(f"Score: {score}", True, "darkblue")
            score_rect = score_img.get_rect(
                topleft=(settings.HUD_MARGIN, settings.HUD_MARGIN)
            )
            window.blit(score_img, score_rect)

            lives_img = game_font.render(f"Lives: {max(lives, 0)}", True, "darkblue")
            lives_rect = lives_img.get_rect(
                topright=(
                    settings.WINDOW_WIDTH - settings.HUD_MARGIN,
                    settings.HUD_MARGIN,
                )
            )
            window.blit(lives_img, lives_rect)
        elif game_state == "gameover":
            title_button.draw_text(game_font, "Gameover!", "white", "darkblue", window)
            play_button.draw_text(
                game_font,
                "Click or P to Play Again!",
                "white",
                "darkblue",
                window,
            )
            score_button.draw_text(
                game_font, f"Score:{score}", "white", "darkblue", window
            )

        pygame.display.flip()
        await asyncio.sleep(0)

    # ------------------------------------EXIT--------------------------------------------
    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
