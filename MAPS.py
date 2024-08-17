import pygame
import sys

pygame.init
 #colour
BLACK=(255,255,255)
WHITE=(0,0,0)

#screen setup
screen_width=600
screen_height=400
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("ECHOES OF THE MULTIVERSE")

#load background
back_ground=pygame.image.load("game background.jpg")

#game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            screen.fill((0, 0, 0))
screen.blit(back_ground, (0, 0))
pygame.display.update()
pygame.quit
sys.exit

