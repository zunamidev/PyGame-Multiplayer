import pygame
from assets.game import multiplayer
from assets.game import color

pygame.init()


def text_objects(text, font):
    textSurface = font.render(text, True, color.black)
    return textSurface, textSurface.get_rect()


def message(msg):
    largeText = pygame.font.SysFont("assets/fonts/BreeSerif-Regular.ttf", 115)
    TextSurf, TextRect = text_objects(msg, largeText)
    TextRect.center = ((multiplayer.display_width / 2), (multiplayer.display_height / 2))
    multiplayer.gameDisplay.blit(TextSurf, TextRect)