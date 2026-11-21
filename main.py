import asyncio
import random

import pygame

import settings
import ui
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
    # fonts
    game_font = pygame.font.Font(None, settings.FONT_SIZE)
    title_font = pygame.font.Font(None, settings.TITLE_FONT_SIZE)
    small_font = pygame.font.Font(None, settings.SMALL_FONT_SIZE)

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
    for sound in (hit_sound, game_over_sound):
        sound.set_volume(settings.SFX_VOLUME)
    shoot_sound.set_volume(settings.SHOOT_VOLUME)
    explosion_sound.set_volume(settings.EXPLOSION_VOLUME)

    # background music
    pygame.mixer.music.load(settings.MUSIC)
    pygame.mixer.music.set_volume(settings.MUSIC_VOLUME)

    # play button (used on the menu and game over screens)
    play_button = Button(
        settings.PLAY_BUTTON_Y, game_font, settings.TEXT_COLOR, settings.BUTTON_COLOR
    )

    # menu and game over layout
    center_x = settings.WINDOW_WIDTH // 2
    panel_rect = pygame.Rect(0, 0, settings.PANEL_WIDTH, settings.PANEL_HEIGHT)
    panel_rect.center = (center_x, settings.PANEL_CENTER_Y)
    panel_img = ui.make_panel(
        panel_rect.size, settings.PANEL_COLOR, settings.PANEL_ALPHA
    )

    # pause button: the drawn rect, and a slightly bigger rect for easier tapping
    pause_rect = pygame.Rect(
        0, 0, settings.PAUSE_BUTTON_SIZE, settings.PAUSE_BUTTON_SIZE
    )
    pause_rect.topright = (
        settings.WINDOW_WIDTH - settings.HUD_MARGIN,
        settings.PAUSE_BUTTON_TOP,
    )
    pause_hit_rect = pause_rect.inflate(
        settings.PAUSE_BUTTON_PADDING * 2, settings.PAUSE_BUTTON_PADDING * 2
    )
    pause_img = ui.make_pause_icon(
        settings.PAUSE_BUTTON_SIZE,
        settings.PANEL_COLOR,
        settings.PAUSE_BUTTON_ALPHA,
        settings.TEXT_COLOR,
    )

    # red overlay used for the "life lost" flash
    flash = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    flash.fill(settings.HIT_FLASH_COLOR)

    # dark overlay used while the game is paused
    dim = pygame.Surface(
        (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), pygame.SRCALPHA
    )
    dim.fill((0, 0, 0, settings.PAUSE_DIM_ALPHA))

    # loop variable
    running = True
    # window bounds
    window_rect = window.get_rect()
    # bullet list
    bullet_list = []
    # shoot cool down countdown (seconds)
    shoot_timer = 0
    # enemy list
    enemy_list = []
    # enemy creation timer
    enemy_timer = 0
    # life lost feedback countdown (seconds)
    hit_timer = 0
    # current level and level up message countdown (seconds)
    level = 1
    level_timer = 0
    # True while a touch or click that began on the pause button is still held
    pointer_on_button = False

    # player class object
    player = Player()
    # current lives
    lives = settings.PLAYER_MAX_LIVES
    # game states
    game_state = "menu"  # "menu", "playing", "paused" or "gameover"
    # keeping the score
    score = 0
    # best score of this session
    best_score = 0
    new_best = False

    # game loop
    while running:
        dt = clock.tick(settings.FPS) / 1000
        # ---------------------------------INPUT---------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # start or restart from the menu or game over screen
            elif game_state in ("menu", "gameover") and (
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
                hit_timer = 0
                level = 1
                level_timer = 0
                pointer_on_button = False
                bullet_list = []
                enemy_list = []
                player = Player()
                game_state = "playing"
                pygame.mixer.music.play(-1)

            # pause with the on-screen button (touch or mouse)
            elif (
                game_state == "playing"
                and event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and pause_hit_rect.collidepoint(event.pos)
            ):
                pointer_on_button = True
                game_state = "paused"
                pygame.mixer.music.pause()

            # pause with the P key
            elif (
                game_state == "playing"
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_p
            ):
                game_state = "paused"
                pygame.mixer.music.pause()

            # pause automatically when the window or tab loses focus
            elif game_state == "playing" and event.type == pygame.WINDOWFOCUSLOST:
                game_state = "paused"
                pygame.mixer.music.pause()

            # resume with a tap, a click or the P key
            elif game_state == "paused" and (
                (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)
                or (event.type == pygame.KEYDOWN and event.key == pygame.K_p)
            ):
                game_state = "playing"
                pygame.mixer.music.unpause()
                # make the ship ignore the pointer until the finger is released
                player.pointer_armed = False

            # a separate check, so every button release is noticed
            if event.type == pygame.MOUSEBUTTONUP:
                pointer_on_button = False

        if game_state == "playing":
            player.handle_input(pointer_on_button)
            # ---------------------------------UPDATE----------------------------------------

            player.update(dt, window_rect)

            # difficulty grows with the score
            new_level = score // settings.POINTS_PER_LEVEL + 1
            if new_level > level:
                level = new_level
                level_timer = settings.LEVEL_MESSAGE_TIME
            spawn_interval = max(
                settings.MIN_SPAWN_INTERVAL,
                settings.ENEMY_SPAWN_INTERVAL
                - settings.SPAWN_INTERVAL_STEP * (level - 1),
            )
            enemy_speed = min(
                settings.MAX_ENEMY_SPEED,
                settings.ENEMY_SPEED + settings.ENEMY_SPEED_STEP * (level - 1),
            )

            # timers count down in seconds
            shoot_timer -= dt
            hit_timer -= dt
            level_timer -= dt

            # fire a bullet when the player wants to shoot and the cooldown is over
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

            # spawn an enemy at a random x at the top of the screen
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
                    hit_timer = settings.HIT_FLASH_TIME
                    if lives > 0:
                        hit_sound.play()

            # an enemy that gets past the player costs a life
            for enemy in enemy_list[:]:
                if enemy.rect.top > player.rect.bottom:
                    enemy_list.remove(enemy)
                    lives -= 1
                    hit_timer = settings.HIT_FLASH_TIME
                    if lives > 0:
                        hit_sound.play()

            # game over check
            if lives <= 0:
                game_state = "gameover"
                new_best = score > best_score
                if new_best:
                    best_score = score
                game_over_sound.play()
                pygame.mixer.music.stop()

        # --------------------------------DRAW--------------------------------------------
        window.blit(background, (0, 0))

        if game_state == "menu":
            ui.draw_text(
                window,
                title_font,
                "SPACE SHOOTER",
                settings.ACCENT_COLOR,
                (center_x, settings.TITLE_Y),
            )
            window.blit(panel_img, panel_rect)
            ui.draw_text(
                window,
                game_font,
                "HOW TO PLAY",
                settings.TEXT_COLOR,
                (center_x, panel_rect.top + 35),
            )
            for i, line in enumerate(settings.HOW_TO_PLAY_LINES):
                ui.draw_text(
                    window,
                    small_font,
                    line,
                    settings.TEXT_COLOR,
                    (center_x, panel_rect.top + 85 + i * settings.LINE_SPACING),
                )
            ui.draw_text(
                window,
                small_font,
                f"Best score: {best_score}",
                settings.ACCENT_COLOR,
                (center_x, panel_rect.bottom - 25),
            )
            play_button.draw_text("Tap, click or P to Play!", window)
        elif game_state in ("playing", "paused"):
            player.draw(window)

            for bullet in bullet_list:
                bullet.draw(window)

            for enemy in enemy_list:
                enemy.draw(window)

            # HUD: score at the top left, lives at the top right, level in the middle
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

            # pause button, under the lives text
            window.blit(pause_img, pause_rect)

            # life lost feedback: fading red flash and a message
            if hit_timer > 0:
                flash.set_alpha(
                    int(settings.HIT_FLASH_ALPHA * hit_timer / settings.HIT_FLASH_TIME)
                )
                window.blit(flash, (0, 0))
                ui.draw_text(
                    window,
                    game_font,
                    f"Life lost! {lives} left",
                    settings.HUD_COLOR,
                    (center_x, settings.WINDOW_HEIGHT // 3),
                )

            # level up message
            if level_timer > 0:
                ui.draw_text(
                    window,
                    title_font,
                    f"LEVEL {level}",
                    settings.ACCENT_COLOR,
                    (center_x, settings.WINDOW_HEIGHT // 4),
                )

            # pause overlay, drawn last so it sits on top of everything
            if game_state == "paused":
                window.blit(dim, (0, 0))
                ui.draw_text(
                    window,
                    title_font,
                    "PAUSED",
                    settings.ACCENT_COLOR,
                    (center_x, settings.WINDOW_HEIGHT // 2 - 20),
                )
                ui.draw_text(
                    window,
                    small_font,
                    "Tap, click or press P to resume",
                    settings.TEXT_COLOR,
                    (center_x, settings.WINDOW_HEIGHT // 2 + 30),
                )
        elif game_state == "gameover":
            ui.draw_text(
                window,
                title_font,
                "GAME OVER",
                settings.ACCENT_COLOR,
                (center_x, settings.TITLE_Y),
            )
            window.blit(panel_img, panel_rect)
            ui.draw_text(
                window,
                game_font,
                "YOUR SCORE",
                settings.TEXT_COLOR,
                (center_x, panel_rect.top + 50),
            )
            ui.draw_text(
                window,
                title_font,
                str(score),
                settings.TEXT_COLOR,
                (center_x, panel_rect.top + 110),
            )
            if new_best:
                ui.draw_text(
                    window,
                    game_font,
                    "NEW BEST SCORE!",
                    settings.ACCENT_COLOR,
                    (center_x, panel_rect.top + 175),
                )
            else:
                ui.draw_text(
                    window,
                    game_font,
                    f"Best: {best_score}",
                    settings.TEXT_COLOR,
                    (center_x, panel_rect.top + 175),
                )
            play_button.draw_text("Tap, click or P to Retry!", window)

        pygame.display.flip()
        await asyncio.sleep(0)

    # ------------------------------------EXIT--------------------------------------------
    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
