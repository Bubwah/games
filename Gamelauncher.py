import pygame

from snakegame.Snakegame import Snakegame
from racegame.Racegame import Racegame
from rockgame.rock_paper_scissors import Rockgame
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

        self.launcher_bg = pygame.image.load(os.path.join(self.images_filepath, 'green_backdrop.png'))
        self.launcher_bg = pygame.transform.scale(self.launcher_bg, (self.dis_width, self.dis_height))
        self.snake_img = pygame.image.load(os.path.join(self.images_filepath, 'snake_icon.png'))
        self.racecar_img = pygame.image.load(os.path.join(self.images_filepath, 'racecar_icon.png'))
        self.rock_img = pygame.image.load(os.path.join(self.images_filepath, 'play.png'))



    def launch(self):

        self.launcher = True
        small_text = pygame.font.Font('freesansbold.ttf', 50)
        large_text = pygame.font.Font('freesansbold.ttf', 85)

        while self.launcher:
            self.gameDisplay.blit(self.launcher_bg, (0, 0))
            self.message_display("Bubwah's Games")
            snake_button = button.Button(300, 400, self.snake_img, 0.20, self.gameDisplay)
            race_button = button.Button(150, 400, self.racecar_img, 0.20, self.gameDisplay)
            rock_button = button.Button(450, 375, self.rock_img, 0.15, self.gameDisplay)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            if snake_button.clicked:
                self.launch_snakegame()

            if race_button.clicked:
                self.launch_racegame()

            if rock_button.clicked:
                self.launch_rockgame()


            pygame.display.update()

    def message_display(self, text) -> None:
        large_text = pygame.font.Font('freesansbold.ttf', 55)
        text_surf, text_rect = self.draw_text(text, large_text)
        text_rect.center = ((self.dis_width / 2), (self.dis_height / 3))
        self.gameDisplay.blit(text_surf, text_rect)


    def draw_text(self, text, font):
        text_surface = font.render(text, True, self.green)
        return text_surface, text_surface.get_rect()

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



    @staticmethod
    def launch_rockgame():
        rockgame = Rockgame()
        rockgame.game_intro()

        pygame.quit()
        quit()