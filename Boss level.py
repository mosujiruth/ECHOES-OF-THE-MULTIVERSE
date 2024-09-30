#river of my tears
import pygame
from moviepy.editor import VideoFileClip
import numpy as np
import sys
import random

pygame.init()

#Set up display
screen_width = 800
screen_height = 600
window = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE | pygame.SCALED)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sin to Save")

#Load images and setup
def load_image(path, size=None):
    image = pygame.image.load(path)
    if size:
        image = pygame.transform.scale(image, size)
    return image

# Background and player images
bg_image = load_image('lvl7intro.jpg', (screen_width, screen_height))
player1_img = load_image('captainwillie.png', (200, 200))
player2_img = load_image('thanos.png', (150, 150))

# Character images
char_1 = pygame.image.load("ironwarrior.png").convert_alpha()
char_2 = pygame.image.load("captainwillie.png").convert_alpha()
char_3 = pygame.image.load("stormbreak.png").convert_alpha()
char_1 = pygame.transform.scale(char_1, (200, 350))
char_2 = pygame.transform.scale(char_2, (250, 400))
char_3 = pygame.transform.scale(char_3, (200, 350))

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
    Button(100, 110, char_1, "IRON WARRIOR"),
    Button(250, 70, char_2, "CAPTAIN WILLIE"),
    Button(500, 110, char_3, "STORMBREAK")
]

# Game state
show_level_screen = True
char_selection_screen = False
show_start_screen = False
show_instruction_screen = False
video_played = False
game_started = False
selected_character = None
level_display_duration = 1000  # Show for 1 sec
level_start_time = pygame.time.get_ticks()

# Player position and health
player1_x, player1_y = 20, 350  
player2_x, player2_y = 650, 380  
player1_health = 100
player2_health = 100

def toggle_fullscreen():
    global fullscreen, window
    if fullscreen:
        window = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE | pygame.SCALED)
        fullscreen = False
    else:
        window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.SCALED)
        fullscreen = True

# Health bar
def draw_health_bar(health, x, y, width=100, height=20):
    pygame.draw.rect(screen, white, (x, y, width, height))
    pygame.draw.rect(screen, red, (x, y, health, height))

# Level
def draw_level_screen():
    level_bg = load_image('intro.jpg', (screen_width, screen_height))
    screen.blit(level_bg, (0, 0))
    level_text = font.render("Level 6", True, white)
    screen.blit(level_text, (screen_width//2 - level_text.get_width()//2, screen_height//2))
    pygame.display.flip()

# Start
def draw_start_screen():
    screen.blit(bg_image, (0, 0))  
    title_text = font.render("Sin to Save", True, green)
    start_text = small_font.render("Press ENTER to start", True, green)
    screen.blit(title_text, (screen_width//2 - title_text.get_width()//2, screen_height//3))
    screen.blit(start_text, (screen_width//2 - start_text.get_width()//2, screen_height//2))
    pygame.display.flip()

# Instruction 
def draw_instruction_screen():
    instruction_bg = load_image('you.png', (screen_width, screen_height))
    screen.blit(instruction_bg, (0, 0))
    instruction_text = small_font.render("It's time warrior defeat thanos to get power stone", True, blue)
    continue_text = small_font.render("Press SPACE to continue", True, blue)
    screen.blit(instruction_text, (screen_width//2 - instruction_text.get_width()//2, screen_height//4))
    screen.blit(continue_text, (screen_width//2 - continue_text.get_width()//2, screen_height//2))
    pygame.display.flip()

# Character selection 
def draw_char_selection_screen():
    screen.blit(bg_image, (0, 0))
    for button in char_buttons:
        button.draw(screen)
    pygame.display.flip()

# Fighting mechanics - Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = 5
        self.punch = False
        self.kick = False
        self.punch_rect = pygame.Rect(self.rect.x + 100, self.rect.y + 20, 50, 30)  # Punch hitbox
        self.kick_rect = pygame.Rect(self.rect.x + 100, self.rect.y + 60, 70, 30)   # Kick hitbox

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocity
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocity

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        if self.punch:
            pygame.draw.rect(surface, red, self.punch_rect)  # Display punch hitbox
        if self.kick:
            pygame.draw.rect(surface, red, self.kick_rect)   # Display kick hitbox

    def attack_update(self):
        if self.punch:
            self.punch_rect = pygame.Rect(self.rect.x + 100, self.rect.y + 20, 50, 30)  # Update punch hitbox
        else:
            self.punch_rect = pygame.Rect(self.rect.x + 100, self.rect.y + 20, 0, 0)   # Reset hitbox when not punching

        if self.kick:
            self.kick_rect = pygame.Rect(self.rect.x + 100, self.rect.y + 60, 70, 30)  # Update kick hitbox
        else:
            self.kick_rect = pygame.Rect(self.rect.x + 100, self.rect.y + 60, 0, 0)   # Reset hitbox when not kicking

# Sorceress move by logic
def villain_move(villain):
    # Move left and right with boundary checks
    villain.rect.x += villain.velocity
    if villain.rect.left < 0 or villain.rect.right > screen_width:
        villain.velocity *= -1  # Reverse direction
        villain.rect.x = max(0, min(villain.rect.x, screen_width - villain.rect.width))  # Correct position

# Initialize players with selected character images
player1_image = load_image('captainwillie.png', (200, 200))
player2_image = load_image('thanos.png', (200, 200))
player1 = Player(player1_x, player1_y, player1_image)
player2 = Player(player2_x, player2_y, player2_image)
player2.velocity = 3  # Set velocity for the villain

# Load and set up video
video_clip = VideoFileClip("chitauri.mp4")
video_frame_rate = video_clip.fps
video_frame_duration = 1 / video_frame_rate

# Main loop
clock = pygame.time.Clock()
video_frame = None
running = True
video_start_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if char_selection_screen:
                for button in char_buttons:
                    if button.is_clicked(event.pos):
                        selected_character = button.name
                        if selected_character == "IRON WARRIOR":
                            player1_image = load_image('ironwarrior.png', (200, 200))
                        elif selected_character == "CAPTAIN WILLIE":
                            player1_image = load_image('captainwillie.png', (200, 200))
                        elif selected_character == "STORMBREAK":
                            player1_image = load_image('stormbreak.png', (200, 200))
                        player1.image = player1_image
                        char_selection_screen = False
                        show_start_screen = True
                        break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and show_start_screen:
                show_start_screen = False
                show_instruction_screen = True
            elif event.key == pygame.K_SPACE and show_instruction_screen:
                show_instruction_screen = False
                game_started = True

    keys = pygame.key.get_pressed()

    # Game logic based on states
    if show_level_screen:
        if pygame.time.get_ticks() - level_start_time >= level_display_duration:
            show_level_screen = False
            char_selection_screen = True
        else:
            draw_level_screen()
    elif char_selection_screen:
        draw_char_selection_screen()
    elif show_start_screen:
        draw_start_screen()
    elif show_instruction_screen:
        draw_instruction_screen()
    elif game_started:
        # Video playback logic
        current_time = pygame.time.get_ticks() - video_start_time
        frame_number = int(current_time / (1000 * video_frame_duration))
        
        if frame_number < video_clip.reader.nframes:
            video_frame = video_clip.get_frame(frame_number * video_frame_duration)
            video_frame = pygame.surfarray.make_surface(np.transpose(video_frame, (1, 0, 2)))
            screen.blit(video_frame, (0, 0))
        else:
            video_start_time = pygame.time.get_ticks()  # Reset video start time to loop

        # Game logic
        player1.update(keys)
        villain_move(player2)

        # Clear screen and draw players
        screen.fill(black)
        player1.draw(screen)
        player2.draw(screen)

        # Draw health bars at the top of the screen
        draw_health_bar(player1_health, 50, 20)  # Player 1 health bar 
        draw_health_bar(player2_health, screen_width - 150, 20)  # Player 2 health bar 
        
        pygame.display.flip()

    clock.tick(60)

pygame.quit()
