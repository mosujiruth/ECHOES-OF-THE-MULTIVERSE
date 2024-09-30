#blood sweat and tears of tarshni
import pygame
from moviepy.editor import VideoFileClip
import numpy as np
import sys
import random

import pygame.ftfont

pygame.init()

# Set up display
screen_width = 600
screen_height = 400

screen = pygame.display.set_mode((screen_width, screen_height),pygame.FULLSCREEN)
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

player2_img = load_image('sorceress.png', (30, 30))

# Character images
char_1 = pygame.image.load("iron warrior.png").convert_alpha()
char_2 = pygame.image.load("captainwillie.png").convert_alpha()
char_3 = pygame.image.load("stormbreak.png").convert_alpha()
char_1 = pygame.transform.scale(char_1, (100, 100))
char_2 = pygame.transform.scale(char_2, (150, 150))
char_3 = pygame.transform.scale(char_3, (100, 100))

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

char_images = {
        "IRON WARRIOR": char_1,
        "CAPTAIN WILLIE": char_2,
        "STORMBREAK": char_3
    }


# Game state
show_level_screen = True
show_start_screen = False
show_instruction_screen = False
video_played = False
game_started = False
level_display_duration = 1000  # Show for 1 sec
level_start_time = pygame.time.get_ticks()

# Player position and health
player1_x, player1_y = 20, 250  
player2_x, player2_y = 450, 280  
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
# Set fixed coordinates for health bars at the top of the screen
def draw_health_bar(health, x, y, character_name, font_size=16, bar_width=150, bar_height=25):
    health = max(0, min(health, 100))
    scaled_health = health / 100 * bar_width

    pygame.draw.rect(screen, white, (x - 2, y - 2, bar_width + 4, bar_height + 4), 2)  # Border
    pygame.draw.rect(screen, black, (x, y, bar_width, bar_height))  # Background
    pygame.draw.rect(screen, green, (x, y, scaled_health, bar_height))  # Health bar

    font = pygame.font.Font(None, font_size)
    name_text = font.render(character_name, True, white)

    text_x = x + (bar_width - name_text.get_width()) // 2
    text_y = y + (bar_height - name_text.get_height()) // 2

    screen.blit(name_text, (text_x, text_y))


draw_health_bar(player1_health, 50, 20, "Player 1")  
draw_health_bar(player2_health, 500, 20, "Sorceress")  


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
# Instruction 
def draw_instruction_screen():
    instruction_bg = load_image('extract.jpg', (screen_width, screen_height))
    small_font = pygame.font.Font(None, 24)  
    screen.blit(instruction_bg, (0, 0))
    instruction_text = small_font.render("Defeat the sorceress to obtain the mind stone from Vision", True, green)
    continue_text1 = small_font.render("left punch(W),Right punch(e),left kick(s),right kick(d)", True, green)
    continue_text2 = small_font.render("Press SPACE to continue", True, green)
    screen.blit(instruction_text, (screen_width//2 - instruction_text.get_width()//2, screen_height//4))
    screen.blit(continue_text1, (screen_width//2 - continue_text1.get_width()//2, screen_height//3.5))
    screen.blit(continue_text2, (screen_width//2 - continue_text2.get_width()//2, screen_height//2.5))
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

player2_image = load_image('sorceress.png', (200, 200))

player2 = Player(player2_x, player2_y, player2_image)
player2.velocity = 3  

# End Screen
def draw_end_screen(result):
    screen.fill(black)
    end_text = font.render(result, True, green)
    screen.blit(end_text, (screen_width//2 - end_text.get_width()//2, screen_height//3))
    replay_text = small_font.render("Press R to replay or ESC to quit", True, green)
    screen.blit(replay_text, (screen_width//2 - replay_text.get_width()//2, screen_height//2))
    pygame.display.flip()

ironwarrior = Player(50, screen_height - 100, char_1)
captainwillie = Player(50, screen_height - 100, char_2)
stormbreak = Player(50, screen_height - 100, char_3)

def start_level_6(selected_chara):
    global  player1,player2,player1_health,player2_health,show_start_screen,show_level_screen,show_instruction_screen,show_end_screen
    player1=None
    if selected_chara == "IRON WARRIOR":
        player1 = Player(50, screen_height - 100, char_1)
    elif selected_chara == "CAPTAIN WILLIE":
        player1 = Player(50, screen_height - 100, char_2)
    elif selected_chara == "STORMBREAK":
        player1= Player(50, screen_height - 100, char_3)
    else:
        print("Invalid character selected!")
        return
    
    player2 = Player(player2_x, player2_y, player2_image) 
    player1.rect.topleft = (player1_x, player1_y)
    player2.rect.topleft = (player2_x, player2_y)
    level_start_time = pygame.time.get_ticks() 
    video_played = False
    game_started = False 
    # Reset health
    player1_health = 100
    player2_health = 100
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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and show_start_screen:
                show_start_screen = False
                show_level_screen = False
                try:
                    video_clip = VideoFileClip('scarlett.mp4')
                    video_played = True
                    level_start_time = pygame.time.get_ticks()
                except Exception as e:
                    print(f"Error loading video: {e}")
                    running = False
            elif event.key == pygame.K_SPACE and show_instruction_screen and not game_started:
                game_started = True
                show_instruction_screen = False
            elif event.key == pygame.K_r and show_end_screen:
                # Reset game to initial state
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
            show_start_screen = True  # Automatically go to start screen after level display

     elif show_start_screen:
        draw_start_screen()

     elif video_played and not show_instruction_screen:
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
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:  
            show_instruction_screen = True
            video_played = False
        
     elif show_instruction_screen:
        draw_instruction_screen()

     elif game_started:
        keys = pygame.key.get_pressed()
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

        
        screen.blit(fight_bg_image, (0, 0))  
        draw_health_bar(player1_health, 50, 20, "Player 1") 
        draw_health_bar(player2_health, screen_width - 170, 20, "Sorceress")

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
            import level_7
            level_7.start_level_7(selected_chara)
     elif show_end_screen:
        draw_end_screen(end_screen_result)
        
    
     clock.tick(30)

    pygame.quit()
    sys.exit()
