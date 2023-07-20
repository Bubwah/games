import Racegame
import pygame


def launch_racegame():
    racegame = Racegame.Racegame()
    racegame.game_intro()

    pygame.quit()
    quit()


if __name__ == "__main__":
    launch_racegame()
