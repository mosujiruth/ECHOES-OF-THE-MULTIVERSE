#blood sweat an tears of tarshni
import pygame
from moviepy.editor import VideoFileClip
import numpy as np
import sys

pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sin to Save")

# Load images and setup
def load_image(path, size=None):
    image = pygame.image.load(path)
    if size:
        image = pygame.transform.scale(image, size)
    return image

# Background and player images
bg_image = load_image('sintosave.jpg', (screen_width, screen_height))
player1_img = load_image('captainwillie.png', (200, 200))
player2_img = load_image('sorceress.png', (150, 150))

# Character images
char_1 = pygame.image.load("ironwarrior.png").convert_alpha()
char_2 = pygame.image.load("captainwillie.png").convert_alpha()
char_3 = pygame.image.load("stormbreak.png").convert_alpha()
char_1 = pygame.transform.scale(char_1, (170, 150))
char_2 = pygame.transform.scale(char_2, (170, 150))
char_3 = pygame.transform.scale(char_3, (160, 150))

# Font colors
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Button class
class Button:
    def __init__(self, x, y, image, name):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.name = name

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def is_clicked(self, position):
        return self.rect.collidepoint(position)

# Character selection buttons
char_buttons = [
    Button(75, 110, char_1, "IRON WARRIOR"),
    Button(230, 110, char_2, "CAPTAIN WILLIE"),
    Button(380, 110, char_3, "STORMBREAK")
]

# Game state
show_level_screen = True
char_selection_screen = False
show_start_screen = False
show_instruction_screen = False
video_played = False
game_started = False
selected_character = None
level_display_duration = 2000  # Show for 2 sec
level_start_time = pygame.time.get_ticks()

# Player position and health
player1_x, player1_y = 20, 350  
player2_x, player2_y = 650, 380  
player1_health = 100
player2_health = 100

# Health bar
def draw_health_bar(health, x, y):
    pygame.draw.rect(screen, white, (x, y, 100, 20))
    pygame.draw.rect(screen, red, (x, y, health, 20))

# Level screen
def draw_level_screen():
    level_bg = load_image('redevil.jpg', (screen_width, screen_height))
    screen.blit(level_bg, (0, 0))
    level_text = font.render("Level 6", True, blue)
    screen.blit(level_text, (screen_width//2 - level_text.get_width()//2, screen_height//2))
    pygame.display.flip()

# Start screen
def draw_start_screen():
    screen.blit(bg_image, (0, 0))  
    title_text = font.render("Sin to Save", True, green)
    start_text = small_font.render("Press ENTER to start", True, green)
    screen.blit(title_text, (screen_width//2 - title_text.get_width()//2, screen_height//3))
    screen.blit(start_text, (screen_width//2 - start_text.get_width()//2, screen_height//2))
    pygame.display.flip()

# Instruction screen
def draw_instruction_screen():
    instruction_bg = load_image('extract.jpg', (screen_width, screen_height))
    screen.blit(instruction_bg, (0, 0))
    instruction_text = small_font.render("Defeat the sorceress to obtain the mind stone from Vision", True, green)
    continue_text = small_font.render("Press SPACE to continue", True, green)
    screen.blit(instruction_text, (screen_width//2 - instruction_text.get_width()//2, screen_height//3))
    screen.blit(continue_text, (screen_width//2 - continue_text.get_width()//2, screen_height//2))
    pygame.display.flip()

# Character selection screen
def draw_char_selection_screen():
    screen.blit(bg_image, (0, 0))
    for button in char_buttons:
        button.draw(screen)
    pygame.display.flip()

# Main loop
clock = pygame.time.Clock()
video_clip = None
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if char_selection_screen:
                for button in char_buttons:
                    if button.is_clicked(event.pos):
                        selected_character = button.name
                        char_selection_screen = False
                        show_start_screen = True
                        break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and show_start_screen:
                show_start_screen = False
                show_instruction_screen = False
                video_played = False
                game_started = False
                
                # Load and start the video
                try:
                    video_clip = VideoFileClip('C:/Users/Admin/Desktop/level5map/ECHOES-OF-THE-MULTIVERSE/scarlett.mp4')
                    video_played = True
                    level_start_time = pygame.time.get_ticks()
                except Exception as e:
                    print(f"Error loading video: {e}")
                    running = False
            elif event.key == pygame.K_SPACE and show_instruction_screen and video_played:
                game_started = True
                show_instruction_screen = False

    current_time = pygame.time.get_ticks()

    if show_level_screen:
        draw_level_screen()
        if current_time - level_start_time > level_display_duration:
            show_level_screen = False
            char_selection_screen = True
            level_start_time = pygame.time.get_ticks()

    elif char_selection_screen:
        draw_char_selection_screen()

    elif show_start_screen:
        draw_start_screen()

    elif video_played and not show_instruction_screen:
        # Get the current frame based on time
        frame_time = (pygame.time.get_ticks() - level_start_time) / 1000.0
        if frame_time < video_clip.duration:
            frame = video_clip.get_frame(frame_time)
            if frame is not None:
                frame = np.array(frame)
                img_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                screen.blit(pygame.transform.scale(img_surface, (screen_width, screen_height)), (0, 0))
                pygame.display.flip()
        else:
            show_instruction_screen = True
            video_played = False
            level_start_time = pygame.time.get_ticks()

    elif show_instruction_screen:
        draw_instruction_screen()

    elif game_started:
        # Game screen
        screen.blit(bg_image, (0, 0))
        
        # Display selected character
        if selected_character == "IRON WARRIOR":
            screen.blit(load_image('ironwarrior.png', (200, 200)), (player1_x, player1_y))
        elif selected_character == "CAPTAIN WILLIE":
            screen.blit(load_image('captainwillie.png', (200, 200)), (player1_x, player1_y))
        elif selected_character == "STORMBREAK":
            screen.blit(load_image('stormbreak.png', (200, 200)), (player1_x, player1_y))
        
        screen.blit(player2_img, (player2_x, player2_y))

        # Health bars
        draw_health_bar(player1_health, 50, 50)
        draw_health_bar(player2_health, 650, 50)

        pygame.display.flip()

    clock.tick(30)

pygame.quit()
sys.exit()
