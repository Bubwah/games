import pygame
import os
import random
import button

class Rockgame:
    def __init__(self):
        pygame.init()

        self.dis_height = 700
        self.dis_width = 700
        self.black = (0, 0, 0)

        self.file_path = os.path.dirname(os.path.abspath(__file__))
        self.images_filepath = os.path.join(self.file_path, "Images")

        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))
        pygame.display.set_caption("Rock, paper, scissors")

        self.intro_bg = pygame.image.load(os.path.join(self.images_filepath, 'intro_bg.png'))
        self.intro_bg = pygame.transform.scale(self.intro_bg, (self.dis_width, self.dis_height))

        self.start_img = pygame.image.load(os.path.join(self.images_filepath, "play.png"))
        self.exit_img = pygame.image.load(os.path.join(self.images_filepath, "exit_button.png"))

    def draw_text(self, text, font):
        text_surface = font.render(text, True, self.black)
        return text_surface, text_surface.get_rect()
    def game_intro(self):
        pygame.event.clear()
        self.dis.blit(self.intro_bg, (0, 0))
        self.intro = True
        small_text = pygame.font.Font('freesansbold.ttf', 50)
        text_surf, text_rect = self.draw_text("Rock, paper, scissors", small_text)
        text_rect.center = ((self.dis_width / 2), (self.dis_height / 3.5))
        self.dis.blit(text_surf, text_rect)
        pygame.display.update()

        while self.intro:
            start_button = button.Button(350, 350, self.start_img, 0.20, self.dis)
            exit_button = button.Button(150, 400, self.exit_img, 0.04, self.dis)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            if exit_button.clicked:
                pygame.quit()
                quit()

            if start_button.clicked:
                pygame.quit()
                quit()

            pygame.display.update()


