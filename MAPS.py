import pygame
import sys

pygame.init()
pygame.font.init()

BLACK=(255,255,255)
WHITE=(0,0,0)

# will display the screen 
screen_length = 600
screen_height = 400
window = pygame.display.set_mode((screen_length, screen_height))
pygame.display.set_caption("ECHOES OF THE MULTIVERSE")
font = pygame.font.SysFont('Comic Sans', 48)

#display image
image=pygame.image.load("game_bg.webp")
#please display the image
image=pygame.transform.scale(image,(screen_length,screen_height))

#start button
start_img=pygame.image.load("start.png").convert_alpha()
start_img=pygame.transform.scale(start_img,(130,130))


class button:
    def __init__(self, x, y):
        self.image=start_img
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
    def draw(self,surface):
        surface.blit(self.image,(self.rect.x,self.rect.y))    

#button for all
start_button =button(240, 140)


current_page=0
chossing_character=1
current_level=current_page

# loop 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False      
    if event.type == pygame.MOUSEBUTTONDOWN:
            if current_level ==  current_page: 
                print("Start Button Clicked!")
                current_level = chossing_character 
   
    if current_level ==current_page :
        window.blit(image, (0, 0))
        start_button.draw(window)
    elif current_level == chossing_character: 
        window.blit(image,(0,0))
   
    pygame.display.flip()

def chossing_character():
    window.blit(image,(0,0))
    pygame.display.flip()
    
   

 
pygame.quit()
sys.exit