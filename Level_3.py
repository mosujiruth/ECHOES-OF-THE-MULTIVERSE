import pygame
import sys

pygame.init()
pygame.font.init()

class Heroes:
    def __init__ (self,image,x,y):

        self.image=image
        self.x=x
        self.y=y

    def move(self,dx,dy,maze):
        newer_x= self.x + dx
        newer_y= self.y + dy
  
        if maze[newer_y][newer_x] != 'X':
            self.x = newer_x
            self.y = newer_y  
        
        if 0 <= newer_x < len(maze[0]) and 0 <= newer_y < len(maze):
            if maze[newer_y][newer_x] != 'X':
                self.x = newer_x
                self.y = newer_y
    
    def draw(self, windows):
        windows.blit(self.image, (self.x * block_size, self.y * block_size))       


   
   

yellow=(255, 255, 0)

#screen display
screen_length = 600
screen_height = 400
windows = pygame.display.set_mode((screen_length, screen_height))
pygame.display.set_caption("ECHOES OF THE MULTIVERSE")

font = pygame.font.SysFont('Comic Sans', 12)
block_size = 30
char_1 = pygame.image.load("iron warrior.png").convert_alpha()
char_2 = pygame.image.load("captainwillie.png").convert_alpha()
char_3 = pygame.image.load("stormbreak.png").convert_alpha()
char_1 = pygame.transform.scale(char_1, (30, 30))
char_2 = pygame.transform.scale(char_2, (30, 30))
char_3 = pygame.transform.scale(char_3, (30, 30))

char_images = {
        "IRON WARRIOR": char_1,
        "CAPTAIN WILLIE": char_2,
        "STORMBREAK": char_3
    }

#maze
maze =[
"XXXXX XXXXXXXXXXXXXX",
"XX       X         X",
"XX     XXXX     XXXX",
"X                  X",
"XXXXXXXXXXXX       X",
"X      XXXXXXX     X",
"X     XXXXXXXX     X",
"X                  X",                              
"X  XXX     XXXXXXXXX",
"X  XXX             X",
"X     XXXXXXXXXXXXXX",
"X                XXX",
"XXXXXXXXXXXXXXXX    ",
]


image=pygame.image.load("wolverine deadbody.jpg")
image=pygame.transform.scale(image,(screen_length,screen_height))
image_bg=pygame.image.load("steelclawer.png")
image_bg=pygame.transform.scale(image_bg,(80,80))
image_bg_x = len(maze[0]) - 4
image_bg_y = len(maze) - 1
reality_stone=pygame.image.load("reality stone.png")
reality_stone=pygame.transform.scale(reality_stone,(screen_length,screen_height))

def display_message(message, windows):
    text_surface = font.render(message, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(screen_length // 2, screen_height // 2))
    windows.blit(text_surface, text_rect)
    pygame.display.flip()
def start_level_3(selected_chara):
  heroes_image = char_images.get(selected_chara, None)
  if heroes_image is None:
        print("Invalid character selected!")
        return 
  
  hero=Heroes(heroes_image ,5 ,0)


# loop 
  running = True
  level_completed = False
  while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                 hero.move(0,-1,maze)
            elif event.key == pygame.K_DOWN:
                 hero.move(0,1,maze)
            elif event.key == pygame.K_LEFT:
                 hero.move(-1,0,maze)
            elif event.key == pygame.K_RIGHT:
                 hero.move(1,0,maze)                
         
    windows.blit(image, (0, 0)) 
    
     # Draw the maze
    for y, row in enumerate(maze):
        for x, block in enumerate(row):
            if block == "X":
                pygame.draw.rect(windows, (255, 255, 0), (x * block_size, y * block_size, block_size, block_size))
    windows.blit(image_bg, (image_bg_x * block_size, image_bg_y * block_size))
    if hero.x == image_bg_x and hero.y == image_bg_y:
         level_completed=True  
    
    if level_completed:
            windows.blit(reality_stone, (0, 0))
            display_message("YOU HAVE RECEIVED THE STONE",windows)
            pygame.display.flip()
            pygame.time.wait(3000)  # Wait for 3 seconds before closing or moving to the next level
            running = False
            import Level_4
            Level_4.start_level_4(selected_chara)
    hero.draw(windows)
    pygame.display.flip()



  pygame.quit()
  sys.exit()          
