import pygame


def draw_text(surface, font, text, color, center):
    """Render text and draw it centered on the given point."""
    img = font.render(text, True, color)
    rect = img.get_rect(center=center)
    surface.blit(img, rect)


def make_panel(size, color, alpha):
    """Build a semi-transparent rounded panel surface (create once, draw many times)."""
    panel = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(panel, (*color, alpha), panel.get_rect(), border_radius=12)
    return panel


def make_pause_icon(size, bg_color, alpha, icon_color):
    """Build the pause button image: a rounded square with two bars (create once)."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.rect(surf, (*bg_color, alpha), surf.get_rect(), border_radius=10)
    bar_w = size // 6
    bar_h = size // 2
    start_x = (size - 3 * bar_w) // 2
    top = (size - bar_h) // 2
    pygame.draw.rect(surf, icon_color, (start_x, top, bar_w, bar_h))
    pygame.draw.rect(surf, icon_color, (start_x + 2 * bar_w, top, bar_w, bar_h))
    return surf
