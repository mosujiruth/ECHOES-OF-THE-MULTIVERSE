import pygame
import sys

pygame.init()
pygame.font.init()
pygame.mixer.init()

BLACK = (255, 255, 255)
WHITE = (0, 0, 0)
YELLOW = (255, 255, 0)


screen_length = 600
screen_height = 400
fullscreen = False

window = pygame.display.set_mode((screen_length, screen_height), pygame.FULLSCREEN)
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

# Background music setup
pygame.mixer.music.load("TMS Echoverse.mp3")  # Load your background music file here
pygame.mixer.music.play(-1)  # Play indefinitely

# Load button click sound
button_click_sound = pygame.mixer.Sound("Bitter.wav")

# Function to play button click sound
def play_button_click_sound():
    button_click_sound.play()

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
is_fullscreen=False
def toggle_fullscreen():
    global fullscreen, window
    if is_fullscreen:
       window = pygame.display.set_mode((screen_length, screen_height), pygame.FULLSCREEN)
    else:
       window = pygame.display.set_mode((screen_length, screen_height), pygame.RESIZABLE | pygame.SCALED)


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
                    button_click_sound.play()
                    current_level = chossing_character
                elif exit_button.is_clicked(event.pos):
                    button_click_sound.play()
                    running = False


            elif current_level == chossing_character:
                if chara_1.is_clicked(event.pos):
                    button_click_sound.play()
                    selected_chara = "IRON WARRIOR"
                    current_level = level_3
                elif chara_2.is_clicked(event.pos):
                    play_button_click_sound()
                    selected_chara = "CAPTAIN WILLIE"
                    current_level = level_3
                elif chara_3.is_clicked(event.pos):
                    play_button_click_sound()
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
    
     import Level_1
     Level_1.start_level_1(selected_chara)
     

    pygame.display.flip()

pygame.quit()
sys.exit()
