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
        self.bg = pygame.transform.scale(self.bg, (700, 350))
        self.bg_height = self.bg.get_height()

        self.obstacleImg = pygame.image.load("racecar.png")
        self.obstacleImg = pygame.transform.rotate(pygame.transform.scale(self.obstacleImg, (100, 140)), 180)

        self.carImg = pygame.image.load('racecar.png')
        self.carImg = pygame.transform.scale(self.carImg, (100, 140))

        self.truckImg = pygame.image.load('truck.png')
        self.truckImg = pygame.transform.scale(self.truckImg, (100, 200))

        self.start_Img = pygame.image.load("start_button.png")
        self.exit_Img = pygame.image.load("exit_button.png")

        self.tiles = self.display_height / self.bg_height
        self.tiles = int(self.tiles) + 1

        self.introImg = pygame.image.load("introbg.png")
        self.introImg = pygame.transform.scale(self.introImg, (700, 700))

    def draw_car(self, x, y):
        self.gameDisplay.blit(self.carImg, (x, y))

    def draw_obstacle(self, obstacle_x, obstacle_y, obstacle_type):
        if obstacle_type == "truck":
            img = self.truckImg
        else:
            # default obstacle is car
            img = self.obstacleImg
        print(obstacle_x)
        self.gameDisplay.blit(img, (obstacle_x, obstacle_y))

    def draw_text(self, text, font):
        text_surface = font.render(text, True, self.green)
        return text_surface, text_surface.get_rect()

    def message_display(self, text):
        large_text = pygame.font.Font('freesansbold.ttf', 85)
        text_surf, text_rect = self.draw_text(text, large_text)
        text_rect.center = ((self.display_width / 2), (self.display_height / 2))
        self.gameDisplay.blit(text_surf, text_rect)

        pygame.display.update()

        time.sleep(2)

    def crash(self):
        self.message_display('You Crashed')

    def draw_highscore(self, count):
        font = pygame.font.SysFont(None, 25)
        text = font.render("Dodged: " + str(count), True, self.green)
        self.gameDisplay.blit(text, (0, 0))

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
            small_text = pygame.font.Font('freesansbold.ttf', 50)
            large_text = pygame.font.Font('freesansbold.ttf', 85)
            text_surf, text_rect = self.draw_text("Traffic Dodge", large_text)
            text_rect.center = ((self.display_width / 2), (self.display_height / 2))
            self.gameDisplay.blit(text_surf, text_rect)

            if not Path("./highscore.txt"):
                print("is file")

            else:
                with open("highscore.txt") as f:
                    lines = f.readlines()
                text = small_text.render(f"Highscore: {lines[0]}", True, self.green)
                self.gameDisplay.blit(text, [200, 100])
                pygame.display.update()

            if start_button.clicked:
                self.game_loop()

            if exit_button.clicked:
                pygame.quit()

            pygame.display.update()
            self.clock.tick(15)

    def game_loop(self):
        scroll = 0
        x = (self.display_width * 0.45)
        y = (self.display_height * 0.75)
        obstacle_x_list = [30, 160, 300, 440, 570]
        obstacle_dims = {"truck": (self.truckImg.get_width(), self.truckImg.get_height()),
                         "car": (self.obstacleImg.get_width(), self.obstacleImg.get_height())}

        x_change = 0
        obstacle_x = random.choice(obstacle_x_list)

        obstacle_y = -600

        obstacle_speed = 4
        dodged = 0

        game_exit = False

        obstacles = []

        while not game_exit:

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

            if len(obstacles) == 0:
                if random.random() > 0.85:
                    obstacle_type = "truck"
                else:
                    obstacle_type = "car"
                obstacles.append([obstacle_x, obstacle_y, obstacle_type])

            self.draw_car(x, y)

            for obstacle_index in range(len(obstacles)):
                obstacle = obstacles[obstacle_index]
                self.draw_obstacle(obstacle[0], obstacle[1], obstacle[2])
                obstacle[1] += obstacle_speed
                obstacle_width, obstacle_height = obstacle_dims[obstacle[2]]

                if y < obstacle[1] + obstacle_height:
                    print('y crossover')

                    if obstacle[0] < x < obstacle[0] + obstacle_width \
                            or obstacle_x < x + self.car_width < obstacle[0] + obstacle_width:
                        print('x crossover')

                        self.crash()
                        self.display_highscore(dodged)
                        game_exit = True

                if obstacle[1] > self.display_height:
                    del obstacles[obstacle_index]
                    obstacle_y = 0 - obstacle_height
                    obstacle_x = random.choice(obstacle_x_list)

                    dodged += 1
                    obstacle_speed += 0.5

            self.draw_highscore(dodged)

            if x > self.display_width - self.car_width or x < 0:
                self.crash()
                self.display_highscore(dodged)
                game_exit = True

            pygame.display.update()
            self.clock.tick(60)
