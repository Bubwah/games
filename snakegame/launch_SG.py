from Snakegame import Snakegame

import pygame


def launch_snakegame():
    snakegame = Snakegame()
    snakegame.game_intro()

    pygame.quit()
    quit()


if __name__ == "__main__":
    launch_snakegame()
