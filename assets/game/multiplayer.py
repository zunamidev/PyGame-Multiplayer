import pygame
import random
import time
import os
from assets.game import color
from assets.socket import Create

# INITIALIZE PyGame
pygame.init()

display_width = 800
display_height = 600

car_width = 73
car_height = 73

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

carImg = pygame.image.load('assets/img/car1.png')
player2 = pygame.image.load('assets/img/car2.png')
bg = pygame.image.load('assets/img/bg.png')

pause = False


def things_dodged(count):
    font = pygame.font.SysFont("comicsansms", 25)
    text = font.render("Dodged: " + str(count), True, color.black)
    gameDisplay.blit(text, (0, 0))


def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])


def car(x, y):
    gameDisplay.blit(carImg, (x, y))


def car2(x, y):
    gameDisplay.blit(player2, (x, y))


def text_objects(text, font):
    textSurface = font.render(text, True, color.black)
    return textSurface, textSurface.get_rect()


def crash(player):
    largeText = pygame.font.SysFont("assets/fonts/BreeSerif-Regular.ttf", 115)
    TextSurf, TextRect = text_objects(player + " Crashed", largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    while True:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # gameDisplay.fill(color.white)

        button("Play Again", 150, 450, 100, 50, color.green, color.bright_green, multiplayer)
        button("Quit", 550, 450, 100, 50, color.red, color.bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(click)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))
    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


def quitgame():
    pygame.quit()
    quit()


def unpause():
    global pause
    pause = False


def paused():
    largeText = pygame.font.SysFont("comicsansms", 115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    while pause:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # gameDisplay.fill(white)

        button("Continue", 150, 450, 100, 50, color.green, color.bright_green, unpause)
        button("Back to menu!", 550, 450, 100, 50, color.red, color.bright_red, game_intro)

        pygame.display.update()
        clock.tick(15)


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(bg)
        largeText = pygame.font.SysFont("comicsansms", 115)
        TextSurf, TextRect = text_objects("A bit Racey", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!", 150, 450, 100, 50, color.green, color.bright_green, game_loop)
        button("Multiplayer", 350, 450, 100, 50, color.blue, color.bright_blue, multiplayer)
        button("Quit", 550, 450, 100, 50, color.red, color.bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


def game_loop():
    global pause

    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0
    y_change = 0

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 4
    thing_width = 100
    thing_height = 100

    thingCount = 2

    dodged = 0

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_DOWN:
                    y_change = 5
                if event.key == pygame.K_UP:
                    y_change = -5
                if event.key == pygame.K_p:
                    pause = True
                    paused()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        y += y_change
        gameDisplay.blit(bg, [0, 0])

        #  things(thingx, thingy, thingw, thingh, color)
        things(thing_startx, thing_starty, thing_width, thing_height, color.block_color)

        thing_starty += thing_speed
        car(x, y)
        things_dodged(dodged)

        if x > display_width - car_width or x < 0:
            crash("")

        if y > display_height - car_height or y < -1:
            y_change = -5
        elif y > display_height - car_height or y < 10:
            y_change = 5

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)
            dodged += 1
            thing_speed += 1
            thing_width += (dodged * 1.2)

        if thing_starty < y < thing_starty + thing_height or thing_starty < y + car_height < thing_starty + thing_height:
            print('y crossover')

            if thing_startx < x < thing_startx + thing_width or thing_startx < x + car_width < thing_startx + thing_width:
                print('x crossover')
                crash("")

        pygame.display.update()
        clock.tick(60)


def join():
    os.system("python3 assets/socket/Client.py 127.0.0.1 180")
    print("Connectet")

def menu():

    menu = True

    while menu:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(color.white)
        largeText = pygame.font.SysFont("comicsansms", 115)
        TextSurf, TextRect = text_objects("Multiplayer Menu", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)

        button("Localgame!", 150, 450, 100, 50, color.green, color.bright_green, multiplayer)
        button("Online Game", 350, 450, 100, 50, color.blue, color.bright_blue, online)

        pygame.display.update()
        clock.tick(15)


def online():

    online = True

    while online:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(color.white)
        largeText = pygame.font.SysFont("comicsansms", 115)
        TextSurf, TextRect = text_objects("Multiplayer Menu", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)

        button("Localgame!", 150, 450, 100, 50, color.green, color.bright_green, Create.join)

        pygame.display.update()
        clock.tick(15)


def multiplayer():
    global pause

    x = 550
    y = 450
    x_change = 0
    y_change = 0

    x2 = 150
    y2 = 450

    x2_change = 0
    y2_change = 0

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 4
    thing_width = 100
    thing_height = 100

    display_width_c = 600

    thingCount = 2

    dodged = 0

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_DOWN:
                    y_change = 5
                if event.key == pygame.K_UP:
                    y_change = -5

                if event.key == pygame.K_a:
                    x2_change = -5
                if event.key == pygame.K_d:
                    x2_change = 5
                if event.key == pygame.K_w:
                    y2_change = -5
                if event.key == pygame.K_s:
                    y2_change = 5
                if event.key == pygame.K_p:
                    pause = True
                    paused()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    x2_change = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    y2_change = 0

        x += x_change
        y += y_change

        x2 += x2_change
        y2 += y2_change


        gameDisplay.blit(bg, [0, 0])

        #  things(thingx, thingy, thingw, thingh, color)
        things(thing_startx, thing_starty, thing_width, thing_height, color.block_color)

        thing_starty += thing_speed
        car(x, y)
        car2(x2, y2)
        things_dodged(dodged)

        if x > display_width - car_width or x < 0:
            crash("Player1")

        elif x2 > display_width - car_width or x2 < 0:
            crash("Player2")

        if y > display_height - car_height or y < -1:
            y_change = -5
        elif y > display_height - car_height or y < 10:
            y_change = 5

        if y2 > display_height - car_height or y2 < -1:
            y2_change = -5
        elif y2 > display_height - car_height or y2 < 10:
            y2_change = 5

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)
            dodged += 1
            thing_speed += 1
            thing_width += (dodged * 1.2)

        if thing_starty < y < thing_starty + thing_height or thing_starty < y + car_height < thing_starty + thing_height:
            if thing_startx < x < thing_startx + thing_width or thing_startx < x + car_width < thing_startx + thing_width:
                crash("Player1")
        if thing_starty < y2 < thing_starty + thing_height or thing_starty < y2 + car_height < thing_starty + thing_height:
            if thing_startx < x2 < thing_startx + thing_width or thing_startx < x2 + car_width < thing_startx + thing_width:
                crash("Player2")


        pygame.display.update()
        clock.tick(60)
