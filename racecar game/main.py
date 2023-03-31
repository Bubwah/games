import pygame
import time
import random
import button
from pathlib import Path
import os

pygame.init()

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

block_color = (53, 115, 255)

car_width = 73

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()
obstacleImg = pygame.image.load("obstacle.png")
obstacleImg = pygame.transform.scale(obstacleImg, (100,100))
carImg = pygame.image.load('racecar.png')
carImg = pygame.transform.scale(carImg, (100,100))
DEFAULT_IMAGE_SIZE = (100, 100)
start_Img = pygame.image.load("start_button.png")
#obstacleImg.rect = obstacleImg.get_rect()
#obstacleImg.rect.xy = (x,y)

exit_Img = pygame.image.load("exit_button.png")


def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: " + str(count), True, black)
    gameDisplay.blit(text, (0, 0))


def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])


def car(x, y):
    gameDisplay.blit(carImg, (x, y))


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)



def crash():
    message_display('You Crashed')

def high_score(dodged):
    with open('highscore.txt', "r") as f:
        highscore_lines = f.readlines()[0]

    with open("highscore.txt", "w") as v:
        if dodged >= int(highscore_lines):
            v.write(str(dodged))
        else:
            v.write(highscore_lines)

def game_intro():
    intro = True

    while intro:
        gameDisplay.fill(white)
        start_button = button.Button(450, 400, start_Img, 0.20, gameDisplay)
        exit_button = button.Button(100, 400, exit_Img, 0.04, gameDisplay)

        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        smallText = pygame.font.Font('freesansbold.ttf', 50)
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("A bit Racey", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)





        if not Path("./highscore.txt"):
            print("is file")

        else:
            with open("highscore.txt")as f:
                lines = f.readlines()
            text = smallText.render(str(lines), True, black)
            gameDisplay.blit(text, [300,100])
            pygame.display.update()

        if start_button.clicked:
            game_loop()

        if exit_button.clicked:
            pygame.quit()

        pygame.display.update()
        clock.tick(15)


def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 4
    thing_width = 100
    thing_height = 100
    global dodged
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

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        gameDisplay.fill(white)

        things(thing_startx, thing_starty, thing_width, thing_height, block_color)

        thing_starty += thing_speed
        car(x, y)
        things_dodged(dodged)

        if x > display_width - car_width or x < 0:

            crash()
            high_score(dodged)
            gameExit = True

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)
            dodged += 1
            thing_speed += 1
            thing_width += (dodged * 1.2)

        if y < thing_starty + thing_height:
            print('y crossover')

            if thing_startx < x < thing_startx + thing_width \
                    or thing_startx < x + car_width < thing_startx + thing_width:
                print('x crossover')

                crash()
                high_score(dodged)
                gameExit = True

        pygame.display.update()
        clock.tick(60)


game_intro()

pygame.quit()
quit()
