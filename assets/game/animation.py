import pygame
from assets.game import multiplayer


def fade(width, height):
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        multiplayer.things()
        multiplayer.gameDisplay.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(5)