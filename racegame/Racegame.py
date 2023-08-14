import pygame
import random
import time
import os
import button

from pathlib import Path


class Racegame:
    def __init__(self):
        pygame.init()

        self.file_path = os.path.dirname(os.path.abspath(__file__))
        self.highscore_filepath = os.path.join(self.file_path, "highscore.txt")
        self.images_filepath = os.path.join(self.file_path, "Images")

        self.display_width = 700
        self.display_height = 700

        self.green = (0, 200, 0)

        self.car_width = 73

        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Traffic Dodge')
        self.clock = pygame.time.Clock()

        self.bg = pygame.image.load(os.path.join(self.images_filepath, "road2.png")).convert()
        self.bg = pygame.transform.scale(self.bg, (700, 350))
        self.bg_height = self.bg.get_height()

        self.obstacleImg = pygame.image.load(os.path.join(self.images_filepath, "racecar.png"))
        self.obstacleImg = pygame.transform.rotate(pygame.transform.scale(self.obstacleImg, (100, 140)), 180)

        self.carImg = pygame.image.load(os.path.join(self.images_filepath, 'racecar.png'))
        self.carImg = pygame.transform.scale(self.carImg, (100, 140))

        self.truckImg = pygame.image.load(os.path.join(self.images_filepath, 'truck.png'))
        self.truckImg = pygame.transform.scale(self.truckImg, (100, 200))

        self.racecarBlueImg = pygame.image.load(os.path.join(self.images_filepath, 'racecar_blue.png'))
        self.racecarBlueImg = pygame.transform.rotate(pygame.transform.scale(self.racecarBlueImg, (100, 140)), 180)

        self.racecarGreenImg = pygame.image.load(os.path.join(self.images_filepath, 'racecar_green.png'))
        self.racecarGreenImg = pygame.transform.rotate(pygame.transform.scale(self.racecarGreenImg, (100, 140)), 180)

        self.racecarPinkImg = pygame.image.load(os.path.join(self.images_filepath, 'racecar_pink.png'))
        self.racecarPinkImg = pygame.transform.rotate(pygame.transform.scale(self.racecarPinkImg, (100, 140)), 180)

        self.racecarYellowImg = pygame.image.load(os.path.join(self.images_filepath, 'racecar_yellow.png'))
        self.racecarYellowImg = pygame.transform.rotate(pygame.transform.scale(self.racecarYellowImg, (100, 140)), 180)

        self.motorcycleImg = pygame.image.load(os.path.join(self.images_filepath, 'motorcycle.png'))
        self.motorcycleImg = pygame.transform.rotate(pygame.transform.scale(self.motorcycleImg, (90, 130)), 180)

        self.start_Img = pygame.image.load(os.path.join(self.images_filepath, "start_button.png"))
        self.exit_Img = pygame.image.load(os.path.join(self.images_filepath, "exit_button.png"))

        self.tiles = self.display_height / self.bg_height
        self.tiles = int(self.tiles) + 1

        self.introImg = pygame.image.load(os.path.join(self.images_filepath, "introbg.png"))
        self.introImg = pygame.transform.scale(self.introImg, (700, 700))

        self.delete_obstacles = []
        self.obstacle_dict = {"car": [0.2, self.obstacleImg,
                                      (self.obstacleImg.get_width(), self.obstacleImg.get_height())],
                              "green_car": [0.2, self.racecarGreenImg,
                                            (self.racecarGreenImg.get_width(), self.racecarGreenImg.get_height())],
                              "yellow_car": [0.2, self.racecarYellowImg,
                                             (self.racecarYellowImg.get_width(), self.racecarYellowImg.get_height())],
                              "pink_car": [0.2, self.racecarPinkImg,
                                           (self.racecarPinkImg.get_width(), self.racecarPinkImg.get_height())],
                              "blue_car": [0.2, self.racecarBlueImg,
                                           (self.racecarBlueImg.get_width(), self.racecarBlueImg.get_height())],
                              "motorcycle": [0.2, self.motorcycleImg, (60, self.motorcycleImg.get_height())],
                              "truck": [0.05, self.truckImg,
                                        (self.truckImg.get_width(), self.truckImg.get_height())]}

        self.game_exit = False

    def draw_car(self, x, y):
        self.gameDisplay.blit(self.carImg, (x, y))

    def draw_obstacle(self, obstacle_x, obstacle_y, obstacle_type, obstacle_img):
        self.gameDisplay.blit(obstacle_img, (obstacle_x, obstacle_y))

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

    def crash(self, dodged: int):
        self.message_display('You Crashed')
        self.display_highscore(dodged)
        self.game_intro()

    def draw_highscore(self, count):
        font = pygame.font.SysFont(None, 25)
        text = font.render("Dodged: " + str(count), True, self.green)
        self.gameDisplay.blit(text, (0, 0))

    def display_highscore(self, dodged):
        with open(self.highscore_filepath, "r") as f:
            highscore_lines = f.readlines()[0]

        with open(self.highscore_filepath, "w") as v:
            if dodged >= int(highscore_lines):
                v.write(str(dodged))
            else:
                v.write(highscore_lines)

    def game_intro(self):
        pygame.event.clear()
        pygame.mouse.set_pos(self.display_width//2, self.display_height//2)
        intro = True

        while intro:

            self.gameDisplay.blit(self.introImg, (0, 0))
            start_button = button.Button(400, 400, self.start_Img, 0.20, self.gameDisplay)
            exit_button = button.Button(200, 400, self.exit_Img, 0.04, self.gameDisplay)

            for event in pygame.event.get():
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
                with open(self.highscore_filepath) as f:
                    lines = f.readlines()
                text = small_text.render(f"Highscore: {lines[0]}", True, self.green)
                self.gameDisplay.blit(text, [200, 100])
                pygame.display.update()

            if start_button.clicked:
                self.game_loop()

            if exit_button.clicked:
                pygame.quit()
                quit()
            pygame.display.update()
            self.clock.tick(15)

    def game_loop(self):
        self.game_exit = False
        scroll = 0
        x = (self.display_width * 0.45)
        y = (self.display_height * 0.75)
        obstacle_x_list = [30, 160, 300, 440, 570]

        x_change = 0
        dodged = 0

        obstacles = []

        while not self.game_exit:
            obstacle_speed = min(6 + 0.4 * dodged, 16)
            spawnrate = min(0.02 + 0.008 * dodged, 0.33)
            max_cars = min(dodged // 10 + 1, 3)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_exit = True

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

            if random.random() < spawnrate and len(obstacles) < max_cars:
                random_obstacle = random.choices([(k, v) for k, v in self.obstacle_dict.items()],
                                                 weights=[obst[0] for obst in self.obstacle_dict.values()],
                                                 k=1)[0]
                random_obstacle_type = random_obstacle[0]
                # values: [spawnrate, img, (img_width, img_height)]
                random_obstacle_values = random_obstacle[1]
                random_obstacle_img = random_obstacle_values[1]
                obstacle_dims = random_obstacle_values[2]

                spawn_x = random.choice(obstacle_x_list)
                while spawn_x in [obstacle[0] for obstacle in obstacles if obstacle[1] < obstacle_dims[1]]:
                    spawn_x = random.choice(obstacle_x_list)

                obstacles.append([spawn_x, -600, random_obstacle_type, random_obstacle_img])

            self.draw_car(x, y)

            for obstacle_index in range(len(obstacles)):
                obstacle = obstacles[obstacle_index]
                self.draw_obstacle(obstacle[0], obstacle[1], obstacle[2], obstacle[3])
                obstacle[1] += obstacle_speed
                obstacle_width, obstacle_height = self.obstacle_dict[obstacle[2]][2]

                if y < obstacle[1] + obstacle_height:
                    print('y crossover')

                    if obstacle[0] < x < obstacle[0] + obstacle_width \
                            or obstacle[0] < x + self.car_width < obstacle[0] + obstacle_width:
                        print('x crossover')

                        self.crash(dodged)

                if obstacle[1] > self.display_height:
                    self.delete_obstacles.append(obstacle_index)

                    dodged += 1

            self.draw_highscore(dodged)

            for delete_index in self.delete_obstacles[::-1]:
                print(delete_index, self.delete_obstacles, obstacles)
                del obstacles[delete_index]

            self.delete_obstacles = []

            if x > self.display_width - self.car_width or x < 0:
                self.crash(dodged)

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        quit()