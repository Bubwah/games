import os

import pygame
import time

from random import sample
import button


class Snakegame:
    def __init__(self):
        pygame.init()

        self.file_path = os.path.dirname(os.path.abspath(__file__))
        self.highscore_filepath = os.path.join(self.file_path, "highscore.txt")
        self.images_filepath = os.path.join(self.file_path, "Images")

        self.dis_width = 700
        self.dis_height = 700

        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))
        pygame.display.set_caption("Snake")

        self.intro_bg = pygame.image.load(os.path.join(self.images_filepath, 'intro_bg.png'))
        self.intro_bg = pygame.transform.scale(self.intro_bg, (self.dis_width,self.dis_height))

        self.green = (0, 200, 0)
        self.blue = (0, 0, 255)
        self.orange = (255, 165, 0)
        self.red = (255, 0 , 0)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.block_size = 20

        self.background_img = pygame.image.load(os.path.join(self.images_filepath, "grass.png"))
        self.background_img = pygame.transform.scale(self.background_img,(700, 700))

        self.snake_head_img = pygame.image.load(os.path.join(self.images_filepath, 'snake_head.png'))
        self.snake_body_img = pygame.image.load(os.path.join(self.images_filepath, 'snake_body.png'))
        self.snake_body_img = pygame.transform.scale(self.snake_body_img, (self.block_size, self.block_size))
        self.snake_head_img_left = pygame.transform.scale(self.snake_head_img, (self.block_size, self.block_size))
        self.snake_head_img_right = pygame.transform.rotate(self.snake_head_img_left, (180))
        self.snake_head_img_down = pygame.transform.rotate(self.snake_head_img_right, (270))
        self.snake_head_img_up = pygame.transform.rotate(self.snake_head_img_left, (270))

        self.apple_img = pygame.image.load(os.path.join(self.images_filepath, 'apple.png'))
        self.apple_img = pygame.transform.scale(self.apple_img, (self.block_size, self.block_size))
        self.banana_img = pygame.image.load(os.path.join(self.images_filepath, 'banana.png'))
        self.banana_img = pygame.transform.scale(self.banana_img, (self.block_size, self.block_size))
        self.watermelon_img = pygame.image.load(os.path.join(self.images_filepath, 'watermelon.png'))
        self.watermelon_img = pygame.transform.scale(self.watermelon_img, (self.block_size, self.block_size))

        self.on_img = pygame.image.load(os.path.join(self.images_filepath, "on.png"))
        self.on_img = pygame.transform.scale(self.on_img, (self.block_size*1.5, self.block_size))
        self.off_img = pygame.image.load(os.path.join(self.images_filepath, "off.png"))
        self.off_img = pygame.transform.scale(self.off_img, (self.block_size*1.5, self.block_size))
        self.starting_x = 300
        self.starting_y = 300

        self.x_change = 0
        self.y_change = 0


        self.snake_speed = 1
        self.all_coords = []
        for y in range(0, 700, self.block_size):
            for x in range(0, 700, self.block_size):
                self.all_coords.append((x, y))

        # (20, 0)
        self.sampled_coords = sample(self.all_coords, 3)
        self.foodx = self.sampled_coords[0][0]
        self.foody = self.sampled_coords[0][1]
        self.juicy_foodx = self.sampled_coords[1][0]
        self.juicy_foody = self.sampled_coords[1][1]
        self.twirly_foodx = self.sampled_coords[2][0]
        self.twirly_foody = self.sampled_coords[2][1]
        self.twirly_toggle = False
        self.juicy_toggle = False
        self.basic_toggle = True
        self.start_Img = pygame.image.load(os.path.join(self.images_filepath, 'start_button.png'))
        self.exit_Img = pygame.image.load(os.path.join(self.images_filepath, "exit_button.png"))
        self.intro = True
        self.clock = pygame.time.Clock()
        self.toggle_twirly_fruit_button = button.Button(350, 320, self.on_img, 1, self.dis)
        self.toggle_juicy_fruit_button = button.Button(450, 320, self.on_img, 1, self.dis)
        self.toggle_basic_fruit_button = button.Button(250, 320, self.on_img, 1, self.dis)
    def draw_highscore(self, count: int) -> None:
        font = pygame.font.SysFont(None, 25)
        text = font.render("Eaten: " + str(count), True, self.red)
        self.dis.blit(text, (0, 0))

    def display_highscore(self, eaten: int) -> None:
        with open(self.highscore_filepath, "r") as f:
            highscore_lines = f.readlines()[0]

        with open(self.highscore_filepath, "w") as v:
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

    def draw_snake_body(self, snake_list: list[tuple]) -> None:
        for snake_block in snake_list[0:-1]:
            x, y = snake_block
            #pygame.draw.rect(self.dis, self.blue, [x, y, self.block_size, self.block_size])
            self.dis.blit(self.snake_body_img,[x, y, self.block_size, self.block_size ,])

    def draw_snake_head(self, snake_list: list[tuple], latest_key_pressed):
        for snake_block in snake_list:
            if latest_key_pressed == pygame.K_UP:
                x, y = snake_block
                self.dis.blit(self.snake_head_img_up, [x, y, self.block_size, self.block_size])
            if latest_key_pressed == pygame.K_DOWN:
                x, y = snake_block
                self.dis.blit(self.snake_head_img_down, [x, y, self.block_size, self.block_size])
            if latest_key_pressed == pygame.K_LEFT:
                x, y = snake_block
                self.dis.blit(self.snake_head_img_left, [x, y, self.block_size, self.block_size])
            if latest_key_pressed == pygame.K_RIGHT:
                x, y = snake_block
                self.dis.blit(self.snake_head_img_right, [x, y, self.block_size, self.block_size])

    def draw_food(self, image, food_typex: int, food_typey: int, twirly_toggle, juicy_toggle, basic_toggle) -> None:
        #pygame.draw.rect(self.dis, color, [food_typex, food_typey, self.block_size, self.block_size])
        if basic_toggle:
            if image == self.apple_img:
                self.dis.blit(self.apple_img, [food_typex, food_typey])
        if juicy_toggle:
            if image == self.banana_img:
                self.dis.blit(self.banana_img, [food_typex, food_typey])
        if twirly_toggle:
            if image == self.watermelon_img:
                self.dis.blit(self.watermelon_img, [food_typex, food_typey])

    def game_intro(self):
        pygame.event.clear()
        pygame.mouse.set_pos(200, self.dis_height // 2)
        self.reset()

        self.dis.blit(self.intro_bg, (0,0))
        self.intro = True
        smallest_text = pygame.font.Font('freesansbold.ttf', 15)
        smaller_text = pygame.font.Font('freesansbold.ttf', 20)
        small_text = pygame.font.Font('freesansbold.ttf', 50)
        large_text = pygame.font.Font('freesansbold.ttf', 85)
        text_surf, text_rect = self.draw_text("Snake", large_text)
        text_rect.center = ((self.dis_width / 2), (self.dis_height / 3.5))

        self.dis.blit(text_surf, text_rect)
        text_surf, text_rect = self.draw_text("toggle on/off", smaller_text)
        text_rect.center = (370, 260)
        self.dis.blit(text_surf, text_rect)
        text_surf, text_rect = self.draw_text("twirly food", smallest_text)
        text_rect.center = (365, 300)
        self.dis.blit(text_surf, text_rect)
        text_surf, text_rect = self.draw_text("juicy food", smallest_text)
        text_rect.center = (465, 300)
        self.dis.blit(text_surf, text_rect)
        text_surf, text_rect = self.draw_text("basic food", smallest_text)
        text_rect.center = (265, 300)
        self.dis.blit(text_surf, text_rect)

        with open(self.highscore_filepath) as f:
            lines = f.readlines()
        text = small_text.render(f"Highscore: {lines[0]}", True, self.green)
        self.dis.blit(text, [200, 100])
        pygame.display.update()

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
            if self.toggle_twirly_fruit_button.clicked:
                if self.twirly_toggle:
                    self.toggle_twirly_fruit_button.image = self.on_img

                if not self.twirly_toggle:
                    self.toggle_twirly_fruit_button.image = self.off_img

                self.twirly_toggle = not self.twirly_toggle
            if self.toggle_juicy_fruit_button.clicked:
                if self.juicy_toggle:
                    self.toggle_juicy_fruit_button.image = self.on_img
                if not self.juicy_toggle:
                    self.toggle_juicy_fruit_button.image = self.off_img

                self.juicy_toggle = not self.juicy_toggle

            if self.toggle_basic_fruit_button.clicked:
                if self.basic_toggle:
                    self.toggle_basic_fruit_button.image = self.on_img
                if not self.basic_toggle:
                    self.toggle_basic_fruit_button.image = self.off_img

                self.basic_toggle = not self.basic_toggle

            self.toggle_juicy_fruit_button.draw(self.dis)
            self.toggle_twirly_fruit_button.draw(self.dis)
            self.toggle_basic_fruit_button.draw(self.dis)
            pygame.display.update()



    def game_loop(self):
        game_exit = False
        speed = 0
        eaten = 0
        switch_food = 1
        snake_list = [(self.starting_x-2*self.block_size, self.starting_y), (self.starting_x-self.block_size, self.starting_y), (self.starting_x, self.starting_y)]

        latest_key_pressed = ""

        self.x_change = self.block_size * switch_food

        while not game_exit:




            for event in pygame.event.get():


                if event.type == pygame.QUIT:
                    game_exit = True

                if event.type == pygame.KEYDOWN:

                    if latest_key_pressed != pygame.K_RIGHT:
                        if event.key == pygame.K_LEFT:
                            self.x_change = -self.block_size * switch_food
                            self.y_change = 0
                            latest_key_pressed = pygame.K_LEFT



                    if latest_key_pressed != pygame.K_LEFT:
                        if event.key == pygame.K_RIGHT:
                            self.x_change = self.block_size * switch_food
                            self.y_change = 0
                            latest_key_pressed = pygame.K_RIGHT



                    if latest_key_pressed != pygame.K_DOWN:
                        if event.key == pygame.K_UP:
                            self.y_change = -self.block_size * switch_food
                            self.x_change = 0
                            latest_key_pressed = pygame.K_UP


                    if latest_key_pressed != pygame.K_UP:
                        if event.key == pygame.K_DOWN:
                            self.y_change = self.block_size * switch_food
                            self.x_change = 0
                            latest_key_pressed = pygame.K_DOWN






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
            self.dis.blit(self.background_img, (0, 0))


            self.draw_food(self.apple_img, self.foodx, self.foody, self.twirly_toggle, self.juicy_toggle, self.basic_toggle)
            self.draw_food(self.banana_img, self.juicy_foodx, self.juicy_foody, self.twirly_toggle, self.juicy_toggle, self.basic_toggle)
            self.draw_food(self.watermelon_img, self.twirly_foodx, self.twirly_foody, self.twirly_toggle, self.juicy_toggle, self.basic_toggle)


            if snake_list[-1]:
                self.draw_snake_head(snake_list, latest_key_pressed)
            if snake_list[0:-1]:
                self.draw_snake_body(snake_list)

            pygame.display.update()

            # Eat food
            if self.basic_toggle:
                if current_headx == self.foodx and current_heady == self.foody:

                    snake_list.insert(0, (current_headx - self.x_change, current_heady - self.y_change))
                    eaten += 1
                    print("Yummy!!")

                    self.foodx = self.sampled_coords[0][0]
                    self.foody = self.sampled_coords[0][1]
            # gives + 2 points, but + 4 length of snake.
            if self.juicy_toggle:
                if current_headx == self.juicy_foodx and current_heady == self.juicy_foody:
                    snake_list.insert(0, (current_headx - self.x_change, current_heady - self.y_change))
                    snake_list.insert(0, (current_headx - self.x_change, current_heady - self.y_change))
                    snake_list.insert(0, (current_headx - self.x_change, current_heady - self.y_change))
                    snake_list.insert(0, (current_headx - self.x_change, current_heady - self.y_change))
                    eaten += 2
                    print("Mega yummy")

                    self.juicy_foodx = self.sampled_coords[1][0]
                    self.juicy_foody = self.sampled_coords[1][1]
            if self.twirly_toggle:
                if current_headx == self.twirly_foodx and current_heady == self.twirly_foody:
                    snake_list.insert(0, (current_headx - self.x_change, current_heady - self.y_change))
                    snake_list.insert(0, (current_headx - self.x_change, current_heady - self.y_change))
                    switch_food *= -1
                    eaten += 3
                    self.twirly_foodx = self.sampled_coords[2][0]
                    self.twirly_foody = self.sampled_coords[2][1]

            self.draw_highscore(eaten)
            pygame.display.update()
            pygame.time.wait(75)

        pygame.quit()
        quit()
