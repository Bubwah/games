import pygame
import time
import button
import random

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
        self.black = (0, 0, 0)

        self.x1 = self.dis_width / 2
        self.y1 = self.dis_height / 2

        self.snake_block = 10

        self.snake_speed = 20

        self.small_text = pygame.font.Font('freesansbold.ttf', 50)
        self.large_text = pygame.font.Font('freesansbold.ttf', 85)

        self.snake_list = []
        self.snake_length = 1

        self.x1_change = 0
        self.y1_change = 0

        self.Game_Exit = False

        self.start_Img = pygame.image.load('start_button.png')
        self.exit_Img = pygame.image.load("exit_button.png")

        self.foodx = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0
        self.foody = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0

        self.clock = pygame.time.Clock()

        self.intro = True

    def draw_text(self, text, font):
        text_surface = font.render(text, True, self.green)
        return text_surface, text_surface.get_rect()

    def spawn_snake(self):
        for x in self.snake_list:
            pygame.draw.rect(self.dis, self.blue, [x[0], x[1], self.snake_block, self.snake_block])

    def spawn_food(self):
        pygame.draw.rect(self.dis, self.black, [self.foodx, self.foody, self.snake_block, self.snake_block])

    def display_highscore(self):
        with open('highscore.txt', "r") as f:
            highscore_lines = f.readlines()[0]
        with open("highscore.txt", "w") as v:
            if self.snake_length >= int(highscore_lines):
                v.write(str(self.snake_length - 1))
            else:
                v.write(highscore_lines)

    def draw_highscore(self, count):
        font = pygame.font.SysFont(None, 25)
        text = font.render("Maximum Food eaten: " + str(count), True, self.green)
        self.dis.blit(text, (0, 0))

    def game_intro(self):
        self.dis.blit(self.intro_bg, (0,0))
        self.intro = True

        text_surf, text_rect = self.draw_text("Snake", self.large_text)
        text_rect.center = ((self.dis_width / 2), (self.dis_height / 3.5))
        self.dis.blit(text_surf, text_rect)
        self.foodx = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0
        self.foody = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0

        while self.intro:
            start_button = button.Button(400, 400, self.start_Img, 0.20, self.dis)
            exit_button = button.Button(200, 400, self.exit_Img, 0.04, self.dis)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            if exit_button.clicked:
                pygame.quit()
                quit()

            if start_button.clicked:
                self.game_loop()

            self.draw_highscore(self.snake_length)
            pygame.display.update()

    def game_loop(self):

        self.Game_Exit = False

        self.x1 = self.dis_width / 2
        self.y1 = self.dis_height / 2

        self.snake_list = []

        self.x1_change = 0
        self.y1_change = 0

        while not self.Game_Exit:
            self.dis.fill(self.white)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Game_Exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.x1_change = - self.snake_block
                        self.y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        self.x1_change = + self.snake_block
                        self.y1_change = 0
                    elif event.key == pygame.K_UP:
                        self.y1_change = - self.snake_block
                        self.x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        self.y1_change = + self.snake_block
                        self.x1_change = 0

            if self.x1 >= self.dis_width or self.x1 < 0 or self.y1 >= self.dis_height or self.y1 < 0:
                self.Game_Exit = True

            self.x1 += self.x1_change
            self.y1 += self.y1_change

            self.dis.fill(self.white)
            pygame.draw.rect(self.dis, self.black, [self.foodx, self.foody, self.snake_block, self.snake_block])

            snake_head = [self.x1, self.y1]
            self.snake_list.append(snake_head)
            if len(self.snake_list) > self.snake_length:
                del self.snake_list[0]

            for x in self.snake_list[:-1]:
               if x == snake_head:
                 self.Game_Exit = True
            self.spawn_snake()

            if self.x1 == self.foodx and self.y1 == self.foody:
                self.foodx = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0
                self.foody = round(random.randrange(0, self.dis_height - self.snake_block) / 10.0) * 10.0
                self.snake_length += 1

            self.clock.tick(30)
        pygame.display.update()
        text_surf, text_rect = self.draw_text("you lost", self.large_text)
        text_rect.center = ((self.dis_width / 2), (self.dis_height / 2))
        self.display_highscore()
        self.dis.blit(text_surf, text_rect)
        pygame.display.update()

        time.sleep(4)
        self.game_intro()



