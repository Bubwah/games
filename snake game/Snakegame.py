import pygame
import button
import time
from random import sample
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

        self.starting_x = 300
        self.starting_y = 300

        self.x_change = 0
        self.y_change = 0

        self.block_size = 20
        self.snake_speed = 1

        self.all_coords = []
        for y in range(0, 701, self.block_size):
            for x in range(0, 701, self.block_size):
                self.all_coords.append((x, y))

        # (20, 0)
        self.sampled_coords = sample(self.all_coords, 3)
        self.foodx = self.sampled_coords[0][0]
        self.foody = self.sampled_coords[0][1]
        self.juicy_foodx = self.sampled_coords[1][0]
        self.juicy_foody = self.sampled_coords[1][1]
        self.twirly_foodx = self.sampled_coords[2][0]
        self.twirly_foody = self.sampled_coords[2][1]

        self.start_Img = pygame.image.load('start_button.png')
        self.exit_Img = pygame.image.load("exit_button.png")
        self.intro = True
        self.clock = pygame.time.Clock()

    def draw_highscore(self, count: int) -> None:
        font = pygame.font.SysFont(None, 25)
        text = font.render("Eaten: " + str(count), True, self.green)
        self.dis.blit(text, (0, 0))

    def display_highscore(self, eaten: int) -> None:
        with open('highscore.txt', "r") as f:
            highscore_lines = f.readlines()[0]

        with open("highscore.txt", "w") as v:
            if eaten >= int(highscore_lines):
                v.write(str(eaten))
            else:
                v.write(highscore_lines)

    def reset(self) -> None:
        self.starting_x = 300
        self.starting_y = 300
        self.x_change = 0
        self.y_change = 0

    def message_display(self, text) -> None:
        large_text = pygame.font.Font('freesansbold.ttf', 85)
        text_surf, text_rect = self.draw_text(text, large_text)
        text_rect.center = ((self.dis_width / 2), (self.dis_height / 2))
        self.dis.blit(text_surf, text_rect)

        pygame.display.update()

        time.sleep(2)

    def you_lost(self) -> None:
        self.message_display("you lost")

    def crash(self, eaten: int) -> None:
        self.you_lost()
        self.display_highscore(eaten)
        self.game_intro()

    def snake_crashed(self, current_headx: int, current_heady: int, snake_body: list[tuple]) -> bool:
        #  If snake hit a wall
        if not(0 <= current_headx <= self.dis_width) or not(0 <= current_heady <= self.dis_height):
            return True

        # If snake hit itself
        if (current_headx, current_heady) in snake_body:
            return True

        return False

    def draw_text(self, text, font):
        text_surface = font.render(text, True, self.green)
        return text_surface, text_surface.get_rect()

    def draw_snake(self, snake_list: list[tuple]) -> None:
        for snake_block in snake_list:
            x, y = snake_block
            pygame.draw.rect(self.dis, self.blue, [x, y, self.block_size, self.block_size])

    def draw_food(self, color: tuple, food_typex: int, food_typey: int) -> None:
        pygame.draw.rect(self.dis, color, [food_typex, food_typey, self.block_size, self.block_size])

    def game_intro(self):
        self.reset()

        self.dis.blit(self.intro_bg, (0,0))
        self.intro = True
        small_text = pygame.font.Font('freesansbold.ttf', 50)
        large_text = pygame.font.Font('freesansbold.ttf', 85)
        text_surf, text_rect = self.draw_text("Snake", large_text)
        text_rect.center = ((self.dis_width / 2), (self.dis_height / 3.5))
        self.dis.blit(text_surf, text_rect)

        with open("highscore.txt") as f:
            lines = f.readlines()
        text = small_text.render(f"Highscore: {lines[0]}", True, self.green)
        self.dis.blit(text, [200, 100])
        pygame.display.update()

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
        game_exit = False
        eaten = 0
        switch_food = 1
        snake_list = [(self.starting_x, self.starting_y)]

        while not game_exit:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    game_exit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.x_change = -self.block_size * switch_food
                        self.y_change = 0
                    elif event.key == pygame.K_RIGHT:
                        self.x_change = self.block_size * switch_food
                        self.y_change = 0
                    elif event.key == pygame.K_UP:
                        self.y_change = -self.block_size * switch_food
                        self.x_change = 0
                    elif event.key == pygame.K_DOWN:
                        self.y_change = self.block_size * switch_food
                        self.x_change = 0

            self.sampled_coords = sample(self.all_coords, 3)
            # Update snake position
            for i in range(len(snake_list[:-1])):
                snake_list[i] = snake_list[i + 1]
            snake_list[-1] = (snake_list[-1][0] + self.x_change, snake_list[-1][1] + self.y_change)

            current_headx = snake_list[-1][0]
            current_heady = snake_list[-1][1]

            # Check for crash
            if self.snake_crashed(current_headx, current_heady, snake_list[:-1]):
                self.crash(eaten)

            # Rerender game
            self.dis.fill(self.white)

            self.draw_food(self.black, self.foodx, self.foody)
            self.draw_food(self.red, self.juicy_foodx, self.juicy_foody)
            self.draw_food(self.blue, self.twirly_foodx, self.twirly_foody)
            self.draw_snake(snake_list)
            pygame.display.update()

            # Eat food
            if current_headx == self.foodx and current_heady == self.foody:

                snake_list.insert(0, (current_headx - self.x_change, current_heady - self.y_change))
                eaten += 1
                print("Yummy!!")

                self.foodx = self.sampled_coords[0][0]
                self.foody = self.sampled_coords[0][1]
            # gives + 2 points, but + 4 length of snake.
            if current_headx == self.juicy_foodx and current_heady == self.juicy_foody:
                snake_list.insert(0, (current_headx - self.x_change, current_heady - self.y_change))
                snake_list.insert(0, (current_headx - self.x_change, current_heady - self.y_change))
                snake_list.insert(0, (current_headx - self.x_change, current_heady - self.y_change))
                snake_list.insert(0, (current_headx - self.x_change, current_heady - self.y_change))
                eaten += 2
                print("Mega yummy")

                self.juicy_foodx = self.sampled_coords[1][0]
                self.juicy_foody = self.sampled_coords[1][1]
            if current_headx == self.twirly_foodx and current_heady == self.twirly_foody:
                snake_list.insert(0, (current_headx - self.x_change, current_heady - self.y_change))
                snake_list.insert(0, (current_headx - self.x_change, current_heady - self.y_change))
                switch_food *= -1
                eaten += 2
                self.twirly_foodx = self.sampled_coords[2][0]
                self.twirly_foody = self.sampled_coords[2][1]
            self.draw_highscore(eaten)
            pygame.display.update()
            pygame.time.wait(75)

        pygame.quit()
        quit()