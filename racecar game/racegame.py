import button
import pygame
import random
import time

from pathlib import Path
pygame.init()


class Racegame:
    def __init__(self):
        pygame.init()

        self.display_width = 700
        self.display_height = 700

        self.green = (0, 200, 0)

        self.car_width = 73

        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Traffic Dodge')
        self.clock = pygame.time.Clock()

        self.bg = pygame.image.load("road2.png").convert()
        self.bg = pygame.transform.scale(bg, (700, 350))
        self.bg_height = self.bg.get_height()

        self.obstacleImg = pygame.image.load("racecar.png")
        self.obstacleImg = pygame.transform.rotate(pygame.transform.scale(self.obstacleImg, (100, 140)), 180)
        self.obstacleImg_width = pygame.Surface.get_width(self.obstacleImg)
        self.obstacleImg_height = pygame.Surface.get_height(self.obstacleImg)

        self.carImg = pygame.image.load('racecar.png')
        self.carImg = pygame.transform.scale(self.carImg, (100, 140))

        self.start_Img = pygame.image.load("start_button.png")
        self.exit_Img = pygame.image.load("exit_button.png")

        self.tiles = self.display_height / self.bg_height
        self.tiles = int(self.tiles) + 1

        self.introImg = pygame.image.load("introbg.png")
        self.introImg = pygame.transform.scale(self.introImg, (700, 700))

    def things_dodged(self, count):
        font = pygame.font.SysFont('arial', 25)
        text = font.render("Dodged: " + str(count), True, self.green)
        self.gameDisplay.blit(text, (0, 0))

    def car(self, x, y):
        self.gameDisplay.blit(self.carImg, (x, y))

    def obstacle(self, self.obstacleImg, thing_startx, thing_starty):
        self.gameDisplay.blit(self.obstacleImg, (thing_startx, thing_starty))

    def text_objects(self, text, font, color):
        textSurface = font.render(text, True, self.green)
        return textSurface, textSurface.get_rect()

    def message_display(self, text, color):
        largeText = pygame.font.Font('freesansbold.ttf', 85)
        TextSurf, TextRect = text_objects(text, largeText, self.green)
        TextRect.center = ((self.display_width / 2), (self.display_height / 2))
        self.gameDisplay.blit(TextSurf, TextRect)

        pygame.display.update()

        time.sleep(2)

    def crash(self):
        message_display('You Crashed', self.green)

    def display_highscore(self, dodged):
        with open('highscore.txt', "r") as f:
            highscore_lines = f.readlines()[0]

        with open("highscore.txt", "w") as v:
            if dodged >= int(highscore_lines):
                v.write(str(dodged))
            else:
                v.write(highscore_lines)

    def game_intro(self):
        intro = True

        while intro:
            self.gameDisplay.blit(self.introImg, (0, 0))
            start_button = button.Button(400, 400, self.start_Img, 0.20, self.gameDisplay)
            exit_button = button.Button(200, 400, self.exit_Img, 0.04, self.gameDisplay)

            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            smallText = pygame.font.Font('freesansbold.ttf', 50)
            largeText = pygame.font.Font('freesansbold.ttf', 85)
            TextSurf, TextRect = text_objects("Traffic Dodge", largeText, self.green)
            # TextSurf, TextRect = text_objects(largeText.render("A bit Racey", True, self.green), largeText)
            TextRect.center = ((self.display_width / 2), (self.display_height / 2))
            self.gameDisplay.blit(TextSurf, TextRect)

            if not Path("./highscore.txt"):
                print("is file")

            else:
                with open("highscore.txt") as f:
                    lines = f.readlines()
                text = smallText.render(f"Highscore: {lines[0]}", True, self.green)
                self.gameDisplay.blit(text, [200, 100])
                pygame.display.update()

            if start_button.clicked:
                game_loop()

            if exit_button.clicked:
                pygame.quit()

            pygame.display.update()
            self.clock.tick(15)

    def game_loop(self):
        scroll = 0
        x = (self.display_width * 0.45)
        y = (self.display_height * 0.75)

        x_change = 0
        thing_startx = random.randrange(0, self.display_width - 100)
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
            for i in range(self.tiles - 2, -2, -1):
                self.gameDisplay.blit(self.bg, (0, i * self.bg_height + scroll))

            scroll += 3
            if abs(scroll) > self.bg_height:
                scroll = 0
            obstacle(self.obstacleImg, thing_startx, thing_starty)

            thing_starty += thing_speed
            car(x, y)
            things_dodged(dodged)

            if x > self.display_width - self.car_width or x < 0:
                crash()
                display_highscore(dodged)
                gameExit = True

            if thing_starty > self.display_height:
                thing_starty = 0 - self.obstacleImg_height
                thing_startx = random.randrange(0, self.display_width - 100)
                dodged += 1
                thing_speed += 0.5

            if y < thing_starty + self.obstacleImg_height:
                print('y crossover')

                if thing_startx < x < thing_startx + self.obstacleImg_width \
                        or thing_startx < x + self.car_width < thing_startx + self.obstacleImg_width:
                    print('x crossover')

                    crash()
                    display_highscore(dodged)
                    gameExit = True

            pygame.display.update()
            self.clock.tick(60)


def main():
    racegame = Racegame()
    racegame.game_intro()

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
