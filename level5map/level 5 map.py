#Tarshni muhunthan
import pygame
import sys
import json
pygame.init
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Level 5")

# Load font
font = pygame.font.Font(None, 36)

background_image = pygame.image.load("asgard.jpg")

def start_screen():
     screen.blit(background_image, (0, 0)) 
print("\033[1;32;40m]")
text = font.render("Welcome to asgard,find and fix the tesseract to obtain space stone")
screen.blit(text, (200, 200))
pygame.display.flip() 
pygame.time.delay(3000) 
def main():
    start_screen()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    pygame.quit()
    sys.exit()


