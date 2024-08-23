import pygame
import sys

pygame.init()
pygame.font.init()

yellow=(255, 255, 0)

#screen display
screen_length = 600
screen_height = 400
window = pygame.display.set_mode((screen_length, screen_height))
pygame.display.set_caption("ECHOES OF THE MULTIVERSE")
font = pygame.font.SysFont('Comic Sans', 48)
#maze
maze=[
"XXXXXXXXXXXXXXXXXXXXXXXXXX     ",
"XXXXX                          ",
"XX                             ",
"XX      XXXXXXX              XX",
"XX      XXXXX       XXX      XX",
"XXXX    XXXXX    XXXXX     XXXX",
"XXX     XXXX       XX        XX",
"XXX     XXX         X       XXX",                              
"XXX      XXXX       X       XXX",
"X        XXXXX            XXXXX",
"X        XXXXX        XXXXXXXXX",
"XXX      XXX          XXXXXXXXX",
"X        XXXX         X    XXXX",
"XX                    X    XXXX",
"X                    XX    XXXX",
"XXXX              XXXXX       X",
"XXXX                          X",
"                              X",
"                              X",
"      XXXXXXXXXXXXXXXXXXXXXXXXX",
]

#display image
image=pygame.image.load("wolverine deadbody.jpg")
#please display the image
image=pygame.transform.scale(image,(screen_length,screen_height))
# Maze block size
block_size = 20





# loop 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    window.blit(image, (0, 0)) 
    
     # Draw the maze
    for y, row in enumerate(maze):
        for x, block in enumerate(row):
            if block == "X":
                pygame.draw.rect(window, (255, 255, 0), (x * block_size, y * block_size, block_size, block_size))

   
    
    
    pygame.display.flip()


pygame.quit()
sys.exit           