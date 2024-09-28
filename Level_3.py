import pygame
import sys
from moviepy.editor import VideoFileClip
import numpy as np

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
windows = pygame.display.set_mode((screen_length, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("ECHOES OF THE MULTIVERSE")

font = pygame.font.SysFont('Comic Sans', 12)
block_size = 15
char_1 = pygame.image.load("iron warrior.png").convert_alpha()
char_2 = pygame.image.load("captainwillie.png").convert_alpha()
char_3 = pygame.image.load("stormbreak.png").convert_alpha()
char_1 = pygame.transform.scale(char_1, (15, 15))
char_2 = pygame.transform.scale(char_2, (15, 15))
char_3 = pygame.transform.scale(char_3, (15, 15))

char_images = {
        "IRON WARRIOR": char_1,
        "CAPTAIN WILLIE": char_2,
        "STORMBREAK": char_3
    }

#maze
maze =[
"XXXX   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
"XX                                     X",
"XXXXXXXXXXX   XXXX    XXX     XXX      X",
"X       XXX   XXX     XX     XXXX   XXXX",
"X       XXXX       XXXX      XXXX   XXXX",
"X      XXXXXXX   XXXXX       XXXX   XXXX",
"X     XXXXXXXX   XXXXXXX     XX     XXXX",
"X                            XXXXXXXXXXX",                              
"X  XXX     XXXXXXXXXXX   XXXXXX    XXXXX",
"X  XXX         XXXXXXX   XXXXXX   XXXXXX",
"X  XX    XXXXXXXXXXXXXX  XXXXXXX  XXXXXX",
"X            XXXXXXXXXX   XXXXXX  XXXXXX",
"XXXXXXXXXXXXXX                     XXXXX",
"XXXXXX   XXXXXXXXXXXXXXXXX  XXXXXXXXXXXX",
"XXXXXX               XXXXX  XXXXXXXXXXXX",
"XXXXXXXX     XXXXXX  XXXXX    XXXXXXXXXX",
"XXXXXXX    XXXXXXXXX XXXXXX      XXXXXXX",
"XXXXXXXX   XXXXXXXX  XXXXXXXX   XXXXXXXX",
"XXXX          XXXX    XXXXXXX    XXXXXXX",
"XXXX          XXXX    XXXXXXX    XXXXXXX",
"XXXX        XX                    XXXXXX",
"XXXXXX   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
"XXXXXXX   XXXX      XXXXXXXX   XXXXXXXXX",
"XXXXXXX                        XXXXXXXXX",
"XXXXXXXXXXXX    XXXXXXXXXXXXX          X",
"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX XXXXX",
]


image=pygame.image.load("wolverine deadbody.jpg")
image=pygame.transform.scale(image,(screen_length,screen_height))
image_bg=pygame.image.load("graveyard.png")
image_bg=pygame.transform.scale(image_bg,(block_size,block_size))
image_bg_x = 34
image_bg_y = len(maze) - 1
reality_stone=pygame.image.load("reality stone.png")
reality_stone=pygame.transform.scale(reality_stone,(screen_length,screen_height))

start_screen=0
instruction_screen=1
video_playing=2
game_played=3
current_state=start_screen

def toggle_fullscreen():
    global fullscreen, window
    if fullscreen:
        window = pygame.display.set_mode((screen_length, screen_height), pygame.RESIZABLE | pygame.SCALED)
        fullscreen = False
    else:
        window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.SCALED)
        fullscreen = True

def display_message(message, windows):
    text_surface = font.render(message, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(screen_length // 2, screen_height // 2))
    windows.blit(text_surface, text_rect)
    pygame.display.flip()

def draw_level_screen():
    windows.fill((0, 0, 0))  
    level_bgg = pygame.image.load('mazy.png')  # Load the image
    level_bgg = pygame.transform.scale(level_bgg, (screen_length, screen_height))
    windows.blit(level_bgg, (0, 0))
    level_text = font.render("Level 3", True, yellow)
    windows.blit(level_text, (screen_length//2 - level_text.get_width()//2, screen_height//2))
    pygame.display.flip()
 
def draw_instruction_screen():
    windows.fill((0, 0, 0))  
    instruction_bgg = pygame.image.load("mazy.png")
    instruction_bgg=pygame.transform.scale(instruction_bgg,(screen_length,screen_height))
    small_font = pygame.font.Font(None, 24)  # Change font size to a smaller value
    windows.blit(instruction_bgg, (0, 0))
    instruction_text = small_font.render("Finish the maze to obtain the reality stone", True, yellow)
    continue_text1 = small_font.render("left key(left),Right key(right),up key(up),down key(down)", True, yellow)
    continue_text2 = small_font.render("Press SPACE to continue", True, yellow)
    windows.blit(instruction_text, (screen_length//2 - instruction_text.get_width()//2, screen_height//4))
    windows.blit(continue_text1, (screen_length//2 - continue_text1.get_width()//2, screen_height//3.5))
    windows.blit(continue_text2, (screen_length//2 - continue_text2.get_width()//2, screen_height//2.5))
    pygame.display.flip()

def play_video():
    global current_state
    video_placement = 'opening_door.mp4'
    clip = VideoFileClip(video_placement)
    for frame in clip.iter_frames(fps=30):
        frame_surface = pygame.surfarray.make_surface(np.array(frame))
        frame_surface = pygame.transform.scale(frame_surface, (screen_length, screen_height))
        windows.blit(frame_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(int(1000 / clip.fps))
    
    current_state = game_played  # Set to game played after video ends


def start_level_3(selected_chara):
    global current_state
    heroes_image = char_images.get(selected_chara, None)
    if heroes_image is None:
        print("Invalid character selected!")
        return
    
    hero = Heroes(heroes_image, 5, 0)
    running = True
    level_completed = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if current_state == start_screen:
                    draw_level_screen()
                    if event.key == pygame.K_SPACE:
                        current_state = instruction_screen
                        draw_instruction_screen()
                elif current_state == instruction_screen:
                    if event.key == pygame.K_SPACE:
                        current_state = video_playing
                        play_video()  
                elif current_state == game_played:
                    if event.key == pygame.K_UP:
                        hero.move(0, -1, maze)
                    elif event.key == pygame.K_DOWN:
                        hero.move(0, 1, maze)
                    elif event.key == pygame.K_LEFT:
                        hero.move(-1, 0, maze)
                    elif event.key == pygame.K_RIGHT:
                        hero.move(1, 0, maze)

        
        windows.blit(image, (0, 0)) 
        if current_state == start_screen:
            draw_level_screen()
        elif current_state == instruction_screen:
            draw_instruction_screen()
        elif current_state == game_played:
            # Draw the maze
            for y, row in enumerate(maze):
                for x, block in enumerate(row):
                    if block == "X":
                        pygame.draw.rect(windows, (255, 255, 0), (x * block_size, y * block_size, block_size, block_size))
                        windows.blit(image_bg, (image_bg_x * block_size, image_bg_y * block_size))
                        hero.draw(windows)

            # Check for level completion
        if hero.x == image_bg_x and hero.y == image_bg_y:
                level_completed = True
            
        if level_completed:
                windows.blit(reality_stone, (0, 0))
                display_message("YOU HAVE RECEIVED THE STONE", windows)
                pygame.time.wait(3000)
                running = False
                import Level_4
                Level_4.start_level_4(selected_chara)
        pygame.display.flip()
    pygame.quit()
    sys.exit()
