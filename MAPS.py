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

# Load your image
background_image = pygame.image.load('game bg.webp')

# Reduce the size (e.g., half the original size)
new_width = background_image.get_width() // 2
new_height = background_image.get_height() // 2

# Resize the image
background_image = pygame.transform.scale(background_image, (new_width, new_height))


# Set up the display
screen = pygame.display.set_mode((background_image.get_width(), background_image.get_height()))
pygame.display.set_caption('ECHOES OF THE MULTIVERSE')



# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit



