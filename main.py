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
    game_font = pygame.font.Font(None, settings.FONT_SIZE)
    # background: tile the image once into a surface the size of the window
    tile = pygame.image.load(settings.BACKGROUND_IMAGE).convert()
    background = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    for x in range(0, settings.WINDOW_WIDTH, tile.get_width()):
        for y in range(0, settings.WINDOW_HEIGHT, tile.get_height()):
            background.blit(tile, (x, y))

    # sound effects
    shoot_sound = pygame.mixer.Sound(settings.SHOOT_SOUND)
    explosion_sound = pygame.mixer.Sound(settings.EXPLOSION_SOUND)
    hit_sound = pygame.mixer.Sound(settings.HIT_SOUND)
    game_over_sound = pygame.mixer.Sound(settings.GAME_OVER_SOUND)
    for sound in (shoot_sound, hit_sound, game_over_sound):
        sound.set_volume(settings.SFX_VOLUME)
    explosion_sound.set_volume(settings.EXPLOSION_VOLUME)

    # background music
    pygame.mixer.music.load(settings.MUSIC)
    pygame.mixer.music.set_volume(settings.MUSIC_VOLUME)

    # Button class objects
    title_button = Button(
        settings.TITLE_BUTTON_Y, game_font, settings.TEXT_COLOR, settings.BUTTON_COLOR
    )
    play_button = Button(
        settings.PLAY_BUTTON_Y, game_font, settings.TEXT_COLOR, settings.BUTTON_COLOR
    )
    score_button = Button(
        settings.SCORE_BUTTON_Y, game_font, settings.TEXT_COLOR, settings.BUTTON_COLOR
    )

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
    # current lives
    lives = settings.PLAYER_MAX_LIVES
    # game states
    game_state = "menu"  # "menu", "playing" or "gameover"
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
                lives = settings.PLAYER_MAX_LIVES
                shoot_timer = 0
                enemy_timer = 0
                bullet_list = []
                enemy_list = []
                player = Player()
                game_state = "playing"
                pygame.mixer.music.play(-1)

        if game_state == "playing":
            player.handle_input()
            # ---------------------------------UPDATE----------------------------------------

            player.update(dt, window_rect)

            # difficulty grows with the score
            level = score // settings.POINTS_PER_LEVEL + 1
            spawn_interval = max(
                settings.MIN_SPAWN_INTERVAL,
                settings.ENEMY_SPAWN_INTERVAL
                - settings.SPAWN_INTERVAL_STEP * (level - 1),
            )
            enemy_speed = min(
                settings.MAX_ENEMY_SPEED,
                settings.ENEMY_SPEED + settings.ENEMY_SPEED_STEP * (level - 1),
            )

            # fire a bullet when space is held and the cooldown has finished.
            shoot_timer -= dt
            if player.wants_to_shoot and shoot_timer <= 0:
                bullet_list.append(Bullet(player.rect.midtop))
                shoot_sound.play()
                shoot_timer = settings.PLAYER_SHOOT_COOLDOWN
            # handling movement of the bullet
            for bullet in bullet_list:
                bullet.update(dt)

            # bullet removal from the list
            for bullet in bullet_list[:]:
                if bullet.is_off_screen():
                    bullet_list.remove(bullet)

            # spawn an enemy at a random x at the top of the screen.
            enemy_timer -= dt
            if enemy_timer <= 0:
                enemy_pos = (
                    random.randint(
                        window_rect.left + settings.ENEMY_SPAWN_MARGIN,
                        window_rect.right - settings.ENEMY_SPAWN_MARGIN,
                    ),
                    0,
                )
                enemy_list.append(Enemy(enemy_pos, enemy_speed))
                enemy_timer = spawn_interval

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
                        score += settings.POINTS_PER_KILL
                        explosion_sound.play()
                        break

            # handling enemy and player collision
            for enemy in enemy_list[:]:
                if enemy.rect.colliderect(player.rect):
                    enemy_list.remove(enemy)
                    lives -= 1
                    if lives > 0:
                        hit_sound.play()

            # game over check
            if lives <= 0:
                game_state = "gameover"
                game_over_sound.play()
                pygame.mixer.music.stop()

        # --------------------------------DRAW--------------------------------------------
        window.blit(background, (0, 0))

        if game_state == "menu":
            title_button.draw_text("Welcome Space Shooter!", window)
            play_button.draw_text("Click or press P to Play!", window)
        elif game_state == "playing":
            player.draw(window)

            for bullet in bullet_list:
                bullet.draw(window)

            for enemy in enemy_list:
                enemy.draw(window)

            # HUD: score at the top left, lives at the top right
            score_img = game_font.render(f"Score: {score}", True, settings.HUD_COLOR)
            score_rect = score_img.get_rect(
                topleft=(settings.HUD_MARGIN, settings.HUD_MARGIN)
            )
            window.blit(score_img, score_rect)

            lives_img = game_font.render(
                f"Lives: {max(lives, 0)}", True, settings.HUD_COLOR
            )
            lives_rect = lives_img.get_rect(
                topright=(
                    settings.WINDOW_WIDTH - settings.HUD_MARGIN,
                    settings.HUD_MARGIN,
                )
            )
            window.blit(lives_img, lives_rect)
            level_img = game_font.render(f"Lv {level}", True, settings.HUD_COLOR)
            level_rect = level_img.get_rect(
                midtop=(settings.WINDOW_WIDTH // 2, settings.HUD_MARGIN)
            )
            window.blit(level_img, level_rect)
        elif game_state == "gameover":
            title_button.draw_text("Game Over!", window)
            play_button.draw_text("Click or P to Play Again!", window)
            score_button.draw_text(f"Score: {score}", window)

        pygame.display.flip()
        await asyncio.sleep(0)

    # ------------------------------------EXIT--------------------------------------------
    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
