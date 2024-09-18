#blood sweaat and tears of tarshni
#blood sweaat and tears of tarshni
#blood sweaat and tears of tarshni
import pygame
from moviepy.editor import VideoFileClip
import numpy as np
import sys
import random

pygame.init()

# Set up display
screen_width = 800
screen_height = 600
window = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE | pygame.SCALED)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sin to Save") 

# Load images and setup
def load_image(path, size=None):
    image = pygame.image.load(path)
    if size:
        image = pygame.transform.scale(image, size)
    return image

# Background and player images
fight_bg_image = load_image('firemount.jpg', (screen_width, screen_height))
bg_image = load_image('sintosave.jpg', (screen_width, screen_height))
player1_img = load_image('captainwillie.png', (200, 200))
player2_img = load_image('sorceress.png', (150, 150))

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
screen.blit(fight_bg_image, (0, 0))
# Health bar
def draw_health_bar(health, x, y, character_name, font_size=16, bar_width=100, bar_height=20, offset=40, scale_x=1.0, scale_y=1.0):
    scaled_x = x * scale_x
    scaled_y = y * scale_y
    scale_health = bar_width / 100.0  
    scaled_health = health * scale_health 

    # Draw the background and health bars
    pygame.draw.rect(screen, white, (scaled_x, scaled_y, bar_width * scale_x, bar_height * scale_y))
    pygame.draw.rect(screen, red, (scaled_x, scaled_y, scaled_health, bar_height * scale_y))

    # Create font with specified size
    font = pygame.font.Font(None, font_size)
    name_text = font.render(character_name, True, white)

    # Calculate text position centered within the health bar
    text_x = scaled_x + (bar_width * scale_x - name_text.get_width()) // 2
    text_y = scaled_y + (bar_height * scale_y - name_text.get_height()) // 2

    screen.blit(name_text, (text_x, text_y))


draw_health_bar(75, 50, 50, 'Sorceress', bar_width=120, bar_height=30, scale_x=1.5, scale_y=1.5)

# Level
def draw_level_screen():
    level_bg = load_image('redevil.jpg', (screen_width, screen_height))
    screen.blit(level_bg, (0, 0))
    level_text = font.render("Level 6", True, blue)
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
    instruction_bg = load_image('extract.jpg', (screen_width, screen_height))
    screen.blit(instruction_bg, (0, 0))
    instruction_text = small_font.render("Defeat the sorceress to obtain the mind stone from Vision", True, green)
    continue_text1 = small_font.render("left punch(W),Right punch(e),left kick(s),right kick(d)", True, green)
    continue_text2 = small_font.render("Press SPACE to continue", True, green)
    screen.blit(instruction_text, (screen_width//2 - instruction_text.get_width()//2, screen_height//3))
    screen.blit(continue_text1, (screen_width//2 - continue_text1.get_width()//2, screen_height//2.5))
    screen.blit(continue_text2, (screen_width//2 - continue_text2.get_width()//2, screen_height//1.5))
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
        self.left_punch = False
        self.right_punch = False
        self.left_kick = False
        self.right_kick = False
        self.left_punch_rect = pygame.Rect(self.rect.x - 50, self.rect.y + 20, 50, 30)  # Left punch hitbox
        self.right_punch_rect = pygame.Rect(self.rect.x + 100, self.rect.y + 20, 50, 30)  # Right punch hitbox
        self.left_kick_rect = pygame.Rect(self.rect.x - 70, self.rect.y + 60, 70, 30)  # Left kick hitbox
        self.right_kick_rect = pygame.Rect(self.rect.x + 100, self.rect.y + 60, 70, 30)  # Right kick hitbox

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
        if self.left_punch:
            pygame.draw.rect(surface, red, self.left_punch_rect)  # Display left punch hitbox
        if self.right_punch:
            pygame.draw.rect(surface, red, self.right_punch_rect)  # Display right punch hitbox
        if self.left_kick:
            pygame.draw.rect(surface, red, self.left_kick_rect)   # Display left kick hitbox
        if self.right_kick:
            pygame.draw.rect(surface, red, self.right_kick_rect)   # Display right kick hitbox

    def attack_update(self):
        if self.left_punch:
            self.left_punch_rect = pygame.Rect(self.rect.x - 50, self.rect.y + 20, 50, 30)  # Update left punch hitbox
        else:
            self.left_punch_rect = pygame.Rect(self.rect.x - 50, self.rect.y + 20, 0, 0)   # Reset left punch hitbox

        if self.right_punch:
            self.right_punch_rect = pygame.Rect(self.rect.x + 100, self.rect.y + 20, 50, 30)  # Update right punch hitbox
        else:
            self.right_punch_rect = pygame.Rect(self.rect.x + 100, self.rect.y + 20, 0, 0)   # Reset right punch hitbox

        if self.left_kick:
            self.left_kick_rect = pygame.Rect(self.rect.x - 70, self.rect.y + 60, 70, 30)  # Update left kick hitbox
        else:
            self.left_kick_rect = pygame.Rect(self.rect.x - 70, self.rect.y + 60, 0, 0)   # Reset left kick hitbox

        if self.right_kick:
            self.right_kick_rect = pygame.Rect(self.rect.x + 100, self.rect.y + 60, 70, 30)  # Update right kick hitbox
        else:
            self.right_kick_rect = pygame.Rect(self.rect.x + 100, self.rect.y + 60, 0, 0)   # Reset right kick hitbox

# Villain (Sorceress) movement and attack
def villain_move(villain, player):
    if villain.rect.x > player.rect.x:
        villain.rect.x -= villain.velocity
    elif villain.rect.x < player.rect.x:
        villain.rect.x += villain.velocity

    if villain.rect.y > player.rect.y:
        villain.rect.y -= villain.velocity
    elif villain.rect.y < player.rect.y:
        villain.rect.y += villain.velocity

def villain_attack(villain, attack_timer, player):
    if attack_timer % 60 == 0:  # Attack every second
        direction_x = player.rect.x - villain.rect.x
        direction_y = player.rect.y - villain.rect.y
        distance = max(1, (direction_x ** 2 + direction_y ** 2) ** 0.5)
        direction_x /= distance
        direction_y /= distance
        # Randomly select between punches and kicks
        move = random.choice(['left_punch', 'right_punch', 'left_kick', 'right_kick'])
        if move == 'left_punch':
            villain.left_punch = True
            villain.right_punch = False
            villain.left_punch_rect = pygame.Rect(villain.rect.x - 50 * direction_x, villain.rect.y + 50 * direction_y, 50, 30)
        elif move == 'right_punch':
            villain.right_punch = True
            villain.left_punch = False
            villain.right_punch_rect = pygame.Rect(villain.rect.x + 50 * direction_x, villain.rect.y + 50 * direction_y, 50, 30)
        elif move == 'left_kick':
            villain.left_kick = True
            villain.right_kick = False
            villain.left_kick_rect = pygame.Rect(villain.rect.x - 70 * direction_x, villain.rect.y + 70 * direction_y, 70, 30)
        elif move == 'right_kick':
            villain.right_kick = True
            villain.left_kick = False
            villain.right_kick_rect = pygame.Rect(villain.rect.x + 70 * direction_x, villain.rect.y + 70 * direction_y, 70, 30)

# Initialize players with selected character images
player1_image = load_image('captainwillie.png', (100, 100))
player2_image = load_image('sorceress.png', (200, 200))
player1 = Player(player1_x, player1_y, player1_image)
player2 = Player(player2_x, player2_y, player2_image)
player2.velocity = 3  # Set velocity for the villain


# End Screen
def draw_end_screen(result):
    screen.fill(black)
    end_text = font.render(result, True, green)
    screen.blit(end_text, (screen_width//2 - end_text.get_width()//2, screen_height//3))
    replay_text = small_font.render("Press R to replay or ESC to quit", True, green)
    screen.blit(replay_text, (screen_width//2 - replay_text.get_width()//2, screen_height//2))
    pygame.display.flip()

# Main loop
clock = pygame.time.Clock()
video_clip = None
attack_timer = 0  # Initialize attack timer
running = True
show_end_screen = False
end_screen_result = ""

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
                            player1_image = load_image('captainwillie.png', (250, 250))
                        elif selected_character == "STORMBREAK":
                            player1_image = load_image('stormbreak.png', (200, 200))
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
            elif event.key == pygame.K_r and show_end_screen:
                # Reset the game to the initial state
                player1_health = 100
                player2_health = 100
                player1.rect.topleft = (player1_x, player1_y)
                player2.rect.topleft = (player2_x, player2_y)
                show_end_screen = False
                show_level_screen = True
            elif event.key == pygame.K_ESCAPE and show_end_screen:
                running = False

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
        player1.left_punch = keys[pygame.K_w]  # Left punch
        player1.right_punch = keys[pygame.K_e]  # Right punch
        player1.left_kick = keys[pygame.K_s]  # Left kick
        player1.right_kick = keys[pygame.K_d]  # Right kick
        player1.attack_update()

        # Player 2 (villain) - Automated movement and attack
        villain_move(player2, player1)  # Make the sorceress follow the player
        attack_timer += 1
        villain_attack(player2, attack_timer, player1)  # Villain attacks player in random directions
        player2.attack_update()

        # Collision detection
        if player1.left_punch and player1.left_punch_rect.colliderect(player2.rect):
            player2_health -= 1
            print("Player 1 hit the Sorceress with a left punch!")

        if player1.right_punch and player1.right_punch_rect.colliderect(player2.rect):
            player2_health -= 1
            print("Player 1 hit the Sorceress with a right punch!")

        if player1.left_kick and player1.left_kick_rect.colliderect(player2.rect):
            player2_health -= 2  # Kicks could do more damage
            print("Player 1 hit the Sorceress with a left kick!")

        if player1.right_kick and player1.right_kick_rect.colliderect(player2.rect):
            player2_health -= 2
            print("Player 1 hit the Sorceress with a right kick!")

        if player2.left_punch and player2.left_punch_rect.colliderect(player1.rect):
            player1_health -= 1
            print("Sorceress hit Player 1 with a left punch!")

        if player2.right_punch and player2.right_punch_rect.colliderect(player1.rect):
            player1_health -= 1
            print("Sorceress hit Player 1 with a right punch!")

        if player2.left_kick and player2.left_kick_rect.colliderect(player1.rect):
            player1_health -= 2
            print("Sorceress hit Player 1 with a left kick!")

        if player2.right_kick and player2.right_kick_rect.colliderect(player1.rect):
            player1_health -= 2
            print("Sorceress hit Player 1 with a right kick!")

        # Game screen
        screen.fill(black)
        if selected_character:
            draw_health_bar(player1_health, player1_x, player1_y - 320, selected_character)
        else:
            draw_health_bar(player1_health, player1_x, player1_y - 320, "Player 1", font_size=20)
        draw_health_bar(player2_health, player2_x, player2_y - 340, "Sorceress", font_size=20)
        player1.draw(screen)
        player2.draw(screen)

        pygame.display.flip()

        if player1_health <= 0:
            print("Player 1 has been defeated. Game Over!")
            end_screen_result = "You Lose!"
            show_end_screen = True
            game_started = False

        if player2_health <= 0:
            print("Sorceress has been defeated. You Win!")
            end_screen_result = "You Win!"
            show_end_screen = True
            game_started = False

    elif show_end_screen:
        draw_end_screen(end_screen_result)
    
    clock.tick(30)

pygame.quit()
sys.exit()
