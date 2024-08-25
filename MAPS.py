import pygame
import sys

pygame.init()
pygame.font.init()

BLACK=(255,255,255)
WHITE=(0,0,0)
YELLOW = (255, 255, 0)

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
#character display 
char_1=pygame.image.load("iron warrior.png").convert_alpha()
char_2=pygame.image.load("sorceress.png").convert_alpha()
char_3=pygame.image.load("vision.png").convert_alpha()
char_1=pygame.transform.scale(char_1,(170,150))
char_2=pygame.transform.scale(char_2,(170,150))
char_3=pygame.transform.scale(char_3,(170,150))

charac_names = {
    "IRON WARRIOR": (100, 270),
    "CAPTAIN WILLIE": (250, 270),
    "STORMBREAK": (410, 270)
}

# Font for character names
name_font = pygame.font.SysFont('Comic Sans', 13)

class button:
    def __init__(self, x, y,images):
        self.image=(images)
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
    def draw(self,surface):
        surface.blit(self.image,(self.rect.x,self.rect.y))
    def is_clicked(self, position):
        return self.rect.collidepoint(position)        
    

#button for all
start_button =button(240, 140,start_img)
chara_1=button(75,110,char_1)
chara_2=button(230,110,char_2)
chara_3=button(380,110,char_3)


current_page=0
chossing_character=1
current_level=current_page

selected_chara=None


# loop 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False      
    if event.type == pygame.MOUSEBUTTONDOWN:
            if current_level ==  current_page and start_button.is_clicked(event.pos):
                print("Start Button Clicked!")
                current_level = chossing_character 
            elif current_page == chossing_character:
                if chara_1.is_clicked(event.pos):
                    selected_chara = "IRON WARRIOR"
                elif chara_2.is_clicked(event.pos):
                    selected_chara= "CAPTAIN WILLIE "
                elif chara_3.is_clicked(event.pos):
                    selected_chara="STORMBREAK"   

    
    window.blit(image, (0, 0))   
    if current_level ==current_page :
                start_button.draw(window)
    elif current_level == chossing_character:
        chara_1.draw(window)
        chara_2.draw(window)
        chara_3.draw(window) 
       
       # Draw character names
        for name, pos in charac_names.items():
            name_text = name_font.render(name, True, YELLOW)
            window.blit(name_text, pos)

    pygame.display.flip()


    
   

 
pygame.quit()
sys.exit