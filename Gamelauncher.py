import pygame

from snakegame.Snakegame import Snakegame
from racegame.Racegame import Racegame
import button
import os

class Gamelauncher:
    def __init__(self):
        pygame.init()
        self.dis_width = 700
        self.dis_height = 700
        self.gameDisplay = pygame.display.set_mode((self.dis_width, self.dis_height))

        self.green = (0, 200, 0)

        self.file_path = os.path.dirname(os.path.abspath(__file__))
        self.images_filepath = os.path.join(self.file_path, "Images")

        pygame.display.set_caption("Launcher")

        self.launcher_bg = pygame.image.load(os.path.join(self.images_filepath, 'launcher_bg.png'))
        self.launcher_bg = pygame.transform.scale(self.launcher_bg, (self.dis_width, self.dis_height))
        self.snake_img = pygame.image.load(os.path.join(self.images_filepath, 'snake_icon.png'))
        self.racecar_img = pygame.image.load(os.path.join(self.images_filepath, 'racecar_icon.png'))



    def launch(self):

        self.launcher = True
        small_text = pygame.font.Font('freesansbold.ttf', 50)
        large_text = pygame.font.Font('freesansbold.ttf', 85)

        while self.launcher:
            self.gameDisplay.blit(self.launcher_bg, (0, 0))
            snake_button = button.Button(400, 400, self.snake_img, 0.20, self.gameDisplay)
            race_button = button.Button(200, 400, self.racecar_img, 0.20, self.gameDisplay)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            if snake_button.clicked:
                self.launch_snakegame()

            if race_button.clicked:
                self.launch_racegame()

            pygame.display.update()

    @staticmethod
    def launch_snakegame():
        snakegame = Snakegame()
        snakegame.game_intro()

        pygame.quit()
        quit()

    @staticmethod
    def launch_racegame():
        racegame = Racegame()
        racegame.game_intro()

        pygame.quit()
        quit()