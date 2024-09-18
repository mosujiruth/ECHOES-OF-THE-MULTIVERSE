import pygame
import sys

pygame.init()
pygame.font.init()

BLACK = (255, 255, 255)
WHITE = (0, 0, 0)
YELLOW = (255, 255, 0)


screen_length = 600
screen_height = 400
fullscreen = False

window = pygame.display.set_mode((screen_length, screen_height), pygame.RESIZABLE | pygame.SCALED)
pygame.display.set_caption("ECHOES OF THE MULTIVERSE")
font = pygame.font.SysFont('Comic Sans', 48)

image = pygame.image.load("game_bg.webp")
image = pygame.transform.scale(image, (screen_length, screen_height))

start_img = pygame.image.load("start.png").convert_alpha()
start_img = pygame.transform.scale(start_img, (130, 130))
how_to_play_img = pygame.image.load("HOW_TO_PLAY.png").convert_alpha()
how_to_play_img = pygame.transform.scale(how_to_play_img, (130, 130))
exit_img = pygame.image.load("exit_button.png").convert_alpha()
exit_img = pygame.transform.scale(exit_img, (130, 130))

char_1 = pygame.image.load("iron warrior.png").convert_alpha()
char_2 = pygame.image.load("captainwillie.png").convert_alpha()
char_3 = pygame.image.load("stormbreak.png").convert_alpha()
char_1 = pygame.transform.scale(char_1, (170, 150))
char_2 = pygame.transform.scale(char_2, (170, 150))
char_3 = pygame.transform.scale(char_3, (160, 150))

charac_names = {
    "IRON WARRIOR": (100, 270),
    "CAPTAIN WILLIE": (250, 270),
    "STORMBREAK": (410, 270)
}

# Font for character names
name_font = pygame.font.SysFont('Comic Sans', 13)

class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def is_clicked(self, position):
        return self.rect.collidepoint(position)

# Buttons
start_button = Button(240, 100, start_img)
howtoplay_button = Button(240, 150, how_to_play_img)
exit_button = Button(240, 200, exit_img)
chara_1 = Button(75, 110, char_1)
chara_2 = Button(230, 110, char_2)
chara_3 = Button(380, 110, char_3)


main_menu = 0
chossing_character = 1
how_to_play = 2  
level_3 = 3
current_level = main_menu
selected_chara = None

def toggle_fullscreen():
    global fullscreen, window
    if fullscreen:
        window = pygame.display.set_mode((screen_length, screen_height), pygame.RESIZABLE | pygame.SCALED)
        fullscreen = False
    else:
        window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.SCALED)
        fullscreen = True

def draw_how_to_play():
    instructions = ["Use arrow keys to move", "Press 'space' to attack"]
    y_pos = 100
    for line in instructions:
        instruction_text = font.render(line, True, WHITE)
        window.blit(instruction_text, (50, y_pos))
        y_pos += 50


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                toggle_fullscreen()
            elif event.key == pygame.K_ESCAPE:
                    current_level = main_menu

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_level == main_menu:
                if start_button.is_clicked(event.pos):
                    current_level = chossing_character
                elif exit_button.is_clicked(event.pos):
                    running = False


            elif current_level == chossing_character:
                if chara_1.is_clicked(event.pos):
                    selected_chara = "IRON WARRIOR"
                    current_level = level_3
                elif chara_2.is_clicked(event.pos):
                    selected_chara = "CAPTAIN WILLIE"
                    current_level = level_3
                elif chara_3.is_clicked(event.pos):
                    selected_chara = "STORMBREAK"
                    current_level = level_3

    window.blit(image, (0, 0))

    # Main menu
    if current_level == main_menu:
        start_button.draw(window)
        exit_button.draw(window)
        
    
    elif current_level == chossing_character:
        chara_1.draw(window)
        chara_2.draw(window)
        chara_3.draw(window)

        # Draw character names
        for name, pos in charac_names.items():
            name_text = name_font.render(name, True, YELLOW)
            window.blit(name_text, pos)

    
    elif current_level == level_3 and selected_chara:
    
     import Level_3
     Level_3.start_level_3(selected_chara)

    pygame.display.flip()

pygame.quit()
sys.exit()
