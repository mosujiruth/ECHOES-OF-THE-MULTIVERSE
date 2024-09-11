#blood sweat an tears of tarshni
import pygame
from moviepy.editor import VideoFileClip
import numpy as np
import sys

pygame.init()

# Set up display
screen_width = 800
screen_height = 600
window =pygame.display.set_mode((screen_width, screen_height),pygame.RESIZABLE | pygame.SCALED)
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

def toggle_fullscreen():
    global fullscreen, window
    if fullscreen:
        window = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE | pygame.SCALED)
        fullscreen = False
    else:
        window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.SCALED)
        fullscreen = True


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

# Initialize players with selected character images
player1_image = load_image('captainwillie.png', (100, 100))
player2_image = load_image('sorceress.png', (100, 100))
player1 = Player(player1_x, player1_y, player1_image)
player2 = Player(player2_x, player2_y, player2_image)

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
                        # Update player images based on selected character
                        if selected_character == "IRON WARRIOR":
                            player1_image = load_image('ironwarrior.png', (100, 100))
                        elif selected_character == "CAPTAIN WILLIE":
                            player1_image = load_image('captainwillie.png', (100, 100))
                        elif selected_character == "STORMBREAK":
                            player1_image = load_image('stormbreak.png', (100, 100))
                        player1.image = player1_image
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
            elif event.key == pygame.K_SPACE and show_instruction_screen and not video_played:
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
        keys = pygame.key.get_pressed()

        # Player 1 controls
        player1.update(keys)
        player1.punch = keys[pygame.K_SPACE]
        player1.kick = keys[pygame.K_k]
        player1.attack_update()

        # Player 2 controls (sorceress - AI)
        player2.update(keys)
        player2.punch = pygame.key.get_pressed()[pygame.K_p]
        player2.kick = pygame.key.get_pressed()[pygame.K_l]
        player2.attack_update()

        # Collision detection
        if player1.punch and player1.punch_rect.colliderect(player2.rect):
            player2_health -= 1
            print("Player 1 hit the Sorceress with a punch!")

        if player1.kick and player1.kick_rect.colliderect(player2.rect):
            player2_health -= 2  # Kicks could do more damage
            print("Player 1 hit the Sorceress with a kick!")

        if player2.punch and player2.punch_rect.colliderect(player1.rect):
            player1_health -= 1
            print("Sorceress hit Player 1 with a punch!")

        if player2.kick and player2.kick_rect.colliderect(player1.rect):
            player1_health -= 2  # Kicks could do more damage
            print("Sorceress hit Player 1 with a kick!")

        # Game screen
        screen.fill(black)
        draw_health_bar(player1_health, player1_x, player1_y - 30)
        draw_health_bar(player2_health, player2_x, player2_y - 30)
        player1.draw(screen)
        player2.draw(screen)
        pygame.display.flip()

    clock.tick(30)

pygame.quit()
sys.exit()



    clock.tick(30)

pygame.quit()
sys.exit()
