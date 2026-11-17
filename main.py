import asyncio

import pygame

import settings


async def main():
    # ------------------------------SET UP -----------------------------------------
    pygame.init()
    window = pygame.display.set_mode(
        (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT),
        pygame.RESIZABLE | pygame.SCALED,
    )
    pygame.display.set_caption(settings.WINDOW_CAPTION)
    clock = pygame.time.Clock()

    # variables
    running = True

    # game loop
    while running:
        dt = clock.tick(settings.FPS) / 1000
        # ---------------------------------INPUT---------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # ---------------------------------UPDATE----------------------------------------

        # --------------------------------DRAW--------------------------------------------
        window.fill(settings.BG_COLOR)

        pygame.display.flip()
        await asyncio.sleep(0)

    # ------------------------------------EXIT--------------------------------------------
    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
