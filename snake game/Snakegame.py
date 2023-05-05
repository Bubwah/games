import pygame
import time
import button
pygame.init()

class Snakegame:
    def __init__(self):

        pygame.init()

        self.dis_width = 700
        self.dis_height = 700

        self.dis = pygame.display.set_mode((self.dis_width,self.dis_height))

        pygame.display.update()

        pygame.display.set_caption("Snake")

        self.intro_bg = pygame.image.load('intro_bg.png')
        self.intro_bg = pygame.transform.scale(self.intro_bg, (self.dis_width,self.dis_height))

        self.green = (0, 200, 0)
        self.blue = (0, 0, 255)
        self.red = (255, 0 , 0)
        self.white = (255, 255, 255)

        self.x1 = 300
        self.y1 = 300

        self.x1_change = 0
        self.y1_change = 0

        self.start_Img = pygame.image.load('start_button.png')
        self.exit_Img = pygame.image.load("exit_button.png")

        self.clock = pygame.time.Clock()

    def draw_text(self, text, font):
        text_surface = font.render(text, True, self.green)
        return text_surface, text_surface.get_rect()


    def game_intro(self):
        self.dis.blit(self.intro_bg, (0,0))


        self.intro = True
        small_text = pygame.font.Font('freesansbold.ttf', 50)
        large_text = pygame.font.Font('freesansbold.ttf', 85)
        text_surf, text_rect = self.draw_text("Snake", large_text)
        text_rect.center = ((self.dis_width / 2), (self.dis_height / 3.5))
        self.dis.blit(text_surf, text_rect)

        while self.intro:
            start_button = button.Button(400, 400, self.start_Img, 0.20, self.dis)
            exit_button = button.Button(200, 400, self.exit_Img, 0.04, self.dis)
            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            if exit_button.clicked:
                pygame.quit()
                quit()

            if start_button.clicked:
                self.game_loop()
            pygame.display.update()

    def game_loop(self):
        Game_Exit = False

        while not Game_Exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Game_Exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.x1_change = -10
                        self.y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        self.x1_change = 10
                        self.y1_change = 0
                    elif event.key == pygame.K_UP:
                        self.y1_change == -10
                        self.x1_change == 0
                    elif event.key == pygame.K_DOWN:
                        self.y1_change == 10
                        self.x1_change == 0

            self.x1 += self.x1_change
            self.y1 += self.y1_change

            self.dis.fill(self.white)
            pygame.draw.rect(self.dis, self.blue, [200, 150, 10, 10])
            pygame.display.update()
            self.clock.tick(30)


        pygame.quit()
        quit()


