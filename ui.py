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
