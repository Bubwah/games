import button
import pygame
import random
import time

from pathlib import Path

pygame.init()

display_width = 700
display_height = 700

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 200, 0)
block_color = (53, 115, 255)

car_width = 73

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

bg = pygame.image.load("road2.png").convert()
bg = pygame.transform.scale(bg, (700, 350))
bg_height = bg.get_height()

obstacleImg = pygame.image.load("racecar.png")
obstacleImg = pygame.transform.rotate(pygame.transform.scale(obstacleImg, (100, 140)), 180)
obstacleImg_width = pygame.Surface.get_width(obstacleImg)
obstacleImg_height = pygame.Surface.get_height(obstacleImg)

carImg = pygame.image.load('racecar.png')
carImg = pygame.transform.scale(carImg, (100, 140))

start_Img = pygame.image.load("start_button.png")
exit_Img = pygame.image.load("exit_button.png")

tiles = display_height / bg_height
tiles = int(tiles) + 1

introImg = pygame.image.load("introbg.png")
introImg = pygame.transform.scale(introImg, (700, 700))


def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: " + str(count), True, black)
    gameDisplay.blit(text, (0, 0))


def car(x, y):
    gameDisplay.blit(carImg, (x, y))


def obstacle(obstacleImg, thing_startx, thing_starty):
    gameDisplay.blit(obstacleImg, (thing_startx, thing_starty))


def text_objects(text, font, color):
    textSurface = font.render(text, True, green)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 85)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)


def crash():
    message_display('You Crashed')


def display_highscore(dodged):
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
        gameDisplay.blit(introImg, (0, 0))
        start_button = button.Button(400, 400, start_Img, 0.20, gameDisplay)
        exit_button = button.Button(200, 400, exit_Img, 0.04, gameDisplay)

        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        smallText = pygame.font.Font('freesansbold.ttf', 50)
        largeText = pygame.font.Font('freesansbold.ttf', 85)
        TextSurf, TextRect = text_objects("Traffic Dodge", largeText, green)
        #TextSurf, TextRect = text_objects(largeText.render("A bit Racey", True, green), largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)

        if not Path("./highscore.txt"):
            print("is file")

        else:
            with open("highscore.txt")as f:
                lines = f.readlines()
            text = smallText.render(f"Highscore: {lines[0]}", True, green)
            gameDisplay.blit(text, [200, 100])
            pygame.display.update()

        if start_button.clicked:
            game_loop()

        if exit_button.clicked:
            pygame.quit()

        pygame.display.update()
        clock.tick(15)


def game_loop():
    scroll = 0
    x = (display_width * 0.45)
    y = (display_height * 0.75)

    x_change = 0
    thing_startx = random.randrange(0, display_width - 100)
    thing_starty = -600
    thing_speed = 4
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
        for i in range(tiles-2, -2, -1):
            gameDisplay.blit(bg, (0, i * bg_height + scroll))

        scroll += 3
        if abs(scroll) > bg_height:
            scroll = 0
        obstacle(obstacleImg, thing_startx, thing_starty)

        thing_starty += thing_speed
        car(x, y)
        things_dodged(dodged)

        if x > display_width - car_width or x < 0:

            crash()
            display_highscore(dodged)
            gameExit = True

        if thing_starty > display_height:
            thing_starty = 0 - obstacleImg_height
            thing_startx = random.randrange(0, display_width - 100)
            dodged += 1
            thing_speed += 0.5

        if y < thing_starty + obstacleImg_height:
            print('y crossover')

            if thing_startx < x < thing_startx + obstacleImg_width \
                    or thing_startx < x + car_width < thing_startx + obstacleImg_width:
                print('x crossover')

                crash()
                display_highscore(dodged)
                gameExit = True

        pygame.display.update()
        clock.tick(60)


game_intro()

pygame.quit()
quit()