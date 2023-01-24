import pygame
from start import Download

pygame.init()

text_download = ["loading data...", "drawing text...", "character preparation...", "health check...",
                 "completion of verification..."]
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h


def main(width, height, text_download):
    df = Download(width, height, pygame.font.Font("data/press-start-k.ttf", 50), text_download)
    df.process()


main(width, height, text_download)
