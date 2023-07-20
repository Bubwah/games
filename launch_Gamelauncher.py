import pygame

from Gamelauncher import Gamelauncher


def launch_gamelauncher():
    gamelauncher = Gamelauncher()
    gamelauncher.launch()

    pygame.quit()
    quit()


if __name__ == "__main__":
    launch_gamelauncher()
