from rock_paper_scissors import Rockgame
import pygame

def launch_rockgame():

    rockgame = Rockgame()
    rockgame.game_intro()

    pygame.quit()
    quit()

if __name__ == "__main__":
    launch_rockgame()

