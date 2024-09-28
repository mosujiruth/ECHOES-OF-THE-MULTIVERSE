import pygame
import sys
import random
from moviepy.editor import VideoFileClip
import numpy as np

pygame.init()
pygame.font.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Screen settings
screen_length = 600
screen_height = 400

window = pygame.display.set_mode((screen_length, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("ECHOES OF THE MULTIVERSE")
font = pygame.font.SysFont('Comic Sans', 48)
small_font = pygame.font.SysFont('Comic Sans', 12)

image = pygame.image.load("final battle.png")
image = pygame.transform.scale(image, (screen_length, screen_height))
# Load images

char_1 = pygame.image.load("iron warrior.png").convert_alpha()
char_2 = pygame.image.load("captainwillie.png").convert_alpha()
char_3 = pygame.image.load("stormbreak.png").convert_alpha()
char_1 = pygame.transform.scale(char_1, (100, 100))
char_2 = pygame.transform.scale(char_2, (100, 100))
char_3 = pygame.transform.scale(char_3, (100, 100))
laser_img = pygame.image.load("laser.jpg").convert_alpha()
laser_img = pygame.transform.scale(laser_img, (20, 10))
laptopshot_img = pygame.image.load("willie sheild.jpg").convert_alpha()
laptopshot_img = pygame.transform.scale(laptopshot_img, (20, 10))
thunder_img = pygame.image.load("thunder.jpg").convert_alpha()
thunder_img = pygame.transform.scale(thunder_img, (20, 10))
enemy_photo = pygame.image.load("thanos.png").convert_alpha()
enemy_photo = pygame.transform.scale(enemy_photo, (100, 100))

ironwarrior_credit = pygame.image.load("credit_ironwarrior.png").convert_alpha()
captainwillie_credit = pygame.image.load("credit_captainwillie.png").convert_alpha()
stormbreak_credit = pygame.image.load("credit_stormbreak.png").convert_alpha()


ironwarrior_credit = pygame.transform.scale(ironwarrior_credit, (screen_length, screen_height))
captainwillie_credit = pygame.transform.scale(captainwillie_credit, (screen_length, screen_height))
stormbreak_credit = pygame.transform.scale(stormbreak_credit, (screen_length, screen_height))

button_img = pygame.image.load("s.png").convert_alpha()  # Replace with your button image
button_img = pygame.transform.scale(button_img, (20, 10))  # Resize as needed
button_x = 10  # Adjust this value to move the button horizontally
button_y = 80  # Adjust this value to move the button vertically
button_rect = pygame.Rect(button_x, button_y, button_img.get_width(), button_img.get_height())

char_images = {
    "IRON WARRIOR": char_1,
    "CAPTAIN WILLIE": char_2,
    "STORMBREAK": char_3
}


# Health variables
max_player_health = 100
max_blueskull_health = 300

players_healthy = 100
blueskull_healthy = 300


show_level_screen=True
show_start_screen = False
show_instruction_screen = False
video_played = False
game_started = False
level_display_duration = 1000 
level_start_time = pygame.time.get_ticks()

def draw_level_screen():
    level_bg = pygame.image.load('intro.jpg').convert()  
    level_bg = pygame.transform.scale(level_bg, (screen_length, screen_height)) 
    window.blit(image, (0, 0))
    level_text = font.render("Level 7", True, WHITE)
    window.blit(level_text, (screen_length//2 - level_text.get_width()//2, screen_height//2))
    pygame.display.flip()

# Start
def draw_start_screen():
    window.blit(image, (0, 0))  
    title_text = font.render("WELCOME TO BOSS LEVEL", True,RED )
    start_text = small_font.render("Press ENTER to start", True, RED)
    window.blit(title_text, (screen_length//2 - title_text.get_width()//2, screen_height//3))
    window.blit(start_text, (screen_length//2 - start_text.get_width()//2, screen_height//2))
    pygame.display.flip()

# Instruction 
def draw_instruction_screen():
    instruction_bg = pygame.image.load('you.png').convert()  
    instruction_bg = pygame.transform.scale(instruction_bg, (screen_length, screen_height))  
    window.blit(instruction_bg, (0, 0))
    instruction_text = small_font.render("It's time warrior defeat thanos to get power stone", True, BLACK)
    continue_text = small_font.render("Press SPACE to continue", True, BLACK)
    window.blit(instruction_text, (screen_length//2 - instruction_text.get_width()//2, screen_height//4))
    window.blit(continue_text, (screen_length//2 - continue_text.get_width()//2, screen_height//2))
    pygame.display.flip()

def toggle_fullscreen():
    global fullscreen, window
    if fullscreen:
        window = pygame.display.set_mode((screen_length, screen_height), pygame.RESIZABLE | pygame.SCALED)
        fullscreen = False
    else:
        window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.SCALED)
        fullscreen = True

class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y, image,bullet_image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = 5
        self.jump_velocity = -20
        self.gravity = 1
        self.is_jumping = False
        self.is_blocking = False
        self.punch = False
        self.kick = False
        self.punch_rect = pygame.Rect(self.rect.x + 100, self.rect.y + 20, 50, 30)  # Punch hitbox
        self.kick_rect = pygame.Rect(self.rect.x + 100, self.rect.y + 60, 70, 30)   # Kick hitbox
        self.bullets = [] 
        self.vertical_velocity = 0
        self.bullet_image=bullet_image
        self.special_power_actively= False
        self.special_power_ending_time=0

    def move(self, keys):
        # Movement: left, right
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocity
        
        if self.rect.x < 0:
           self.rect.x = 0
        if self.rect.x > screen_length - self.rect.width:
           self.rect.x = screen_length - self.rect.width
        # Jumping
        if not self.is_jumping and keys[pygame.K_SPACE]:
            self.is_jumping = True
            self.vertical_velocity = self.jump_velocity

        if self.is_jumping:
            self.rect.y += self.vertical_velocity
            self.vertical_velocity += self.gravity
            if self.rect.y >= screen_height - 100:  
                self.rect.y = screen_height - 100
                self.is_jumping = False
                self.vertical_velocity = 0

    def attack(self, keys):
        # Punch
        if keys[pygame.K_a]:
            self.punch = True
        else:
            self.punch = False

        # Kick
        if keys[pygame.K_s]:
            self.kick = True
        else:
            self.kick = False

        # Block
        if keys[pygame.K_d]:
            self.is_blocking = True
        else:
            self.is_blocking = False

    def update_hitboxes(self):
        # Update punch and kick hitboxes
        if self.punch:
            self.punch_rect = pygame.Rect(self.rect.x + 65, self.rect.y + 20, 20, 30)  
        else:
            self.punch_rect = pygame.Rect(self.rect.x + 65, self.rect.y + 20, 0, 0)   

        if self.kick:
            self.kick_rect = pygame.Rect(self.rect.x + 65, self.rect.y + 60, 50, 30)  
        else:
            self.kick_rect = pygame.Rect(self.rect.x + 65, self.rect.y + 60, 0, 0)  

    def activate_special_power(self):
        if len(self.bullets) < 1: 
            print("Special power activated!")  
            bullet = Bullet(self.bullet_image, self.rect.x + 50, self.rect.y + 40, 10) 
            self.bullets.append(bullet)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        if self.punch:
            pygame.draw.rect(surface, RED, self.punch_rect) 
        if self.kick:
            pygame.draw.rect(surface, RED, self.kick_rect)  

        if self.is_blocking:
            pygame.draw.rect(surface, WHITE, self.rect, 3) 
        
        for bullet in self.bullets:
            bullet.draw(surface)

class Bullet:
    def __init__(self, image, x, y, speed):
        self.image = image
        self.x = x
        self.y = y
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, image.get_width(), image.get_height())
    
    def move(self):
        self.x += self.speed
        self.rect.x = self.x  

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

class Titan(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = 3
        self.direction = random.choice([-1, 1])  
        self.is_blocking = False
        self.punch = False
        self.kick = False
        self.action_cooldown = 1000  
        self.move_cooldown = 2000  
        self.last_action_time = pygame.time.get_ticks()
        self.last_move_time = pygame.time.get_ticks()

    def move(self):
       
        if pygame.time.get_ticks() - self.last_move_time > self.move_cooldown:
            self.direction = random.choice([-1, 1])
            self.last_move_time = pygame.time.get_ticks()

        # Move enemy
        self.rect.x += self.velocity * self.direction
        if self.rect.x <= 0:
            self.rect.x = 0
            self.direction = 1
        elif self.rect.x >= screen_length - self.rect.width:
            self.rect.x = screen_length - self.rect.width
            self.direction = -1

    def attack(self):
       
        if pygame.time.get_ticks() - self.last_action_time > self.action_cooldown:
            action = random.randint(1, 100)
            if action < 30:
                self.punch = True
                self.kick = False
                self.is_blocking = False
            elif action < 60:
                self.kick = True
                self.punch = False
                self.is_blocking = False
            elif action < 80:
                self.is_blocking = True
                self.punch = False
                self.kick = False
            else:
                self.punch = False
                self.kick = False
                self.is_blocking = False

            self.last_action_time = pygame.time.get_ticks()  # Reset the action timer
    
    def update_hitboxes(self):
       
        if self.punch:
            self.punch_rect = pygame.Rect(self.rect.x - 20, self.rect.y + 20, 20, 30)  # Update punch hitbox
        else:
            self.punch_rect = pygame.Rect(self.rect.x - 20, self.rect.y + 20, 0, 0)   # Reset hitbox

        if self.kick:
            self.kick_rect = pygame.Rect(self.rect.x - 20, self.rect.y + 60, 50, 30)  # Update kick hitbox
        else:
            self.kick_rect = pygame.Rect(self.rect.x - 20, self.rect.y + 60, 0, 0) 

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        if self.punch:
            pygame.draw.rect(surface, RED, (self.rect.x - 20, self.rect.y + 20, 20, 30))  # Display punch hitbox
        if self.kick:
            pygame.draw.rect(surface, RED, (self.rect.x - 20, self.rect.y + 60, 50, 30))   # Display kick hitbox
        if self.is_blocking:
            pygame.draw.rect(surface, WHITE, self.rect, 3)


def handle_attacks(hero, enemy):
    global players_healthy, blueskull_healthy
    
   
    if hero.punch and hero.punch_rect.colliderect(enemy.rect):
        if not enemy.is_blocking:  
            blueskull_healthy -= 10
        else:
            pass

    if hero.kick and hero.kick_rect.colliderect(enemy.rect):
        if not enemy.is_blocking:
            blueskull_healthy -= 15
        else:
            pass
    
   
    if enemy.punch and enemy.punch_rect.colliderect(hero.rect):
        if not hero.is_blocking:  
            players_healthy -= 10
        else:
            pass
    if enemy.kick and enemy.kick_rect.colliderect(hero.rect):
        if not hero.is_blocking:
            players_healthy -= 15
        else:
            pass

    if hero.is_blocking and enemy.rect.colliderect(hero.rect):
        if enemy.rect.x > hero.rect.x:
            enemy.rect.x = hero.rect.x + hero.rect.width
        else:
            enemy.rect.x = hero.rect.x - enemy.rect.width    

def handle_bullets(hero, enemy):
    global blueskull_healthy

    for bullet in hero.bullets[:]:
        bullet.move()
        if bullet.x > screen_length:  
            hero.bullets.remove(bullet)
        else:
            if bullet.rect.colliderect(enemy.rect):
                blueskull_healthy -= 25  
                hero.bullets.remove(bullet)

ironwarrior = Hero(50, screen_height - 100, char_1,laser_img)
captainwillie = Hero(50, screen_height - 100, char_2,laptopshot_img)
stormbreak = Hero(50, screen_height - 100, char_3,thunder_img)


def show_credits(selected_chara):
    if selected_chara == "IRON WARRIOR":
        window.blit(ironwarrior_credit, (0, 0))
    elif selected_chara == "CAPTAIN WILLIE":
        window.blit(captainwillie_credit, (0, 0))
    elif selected_chara == "STORMBREAK":
        window.blit(stormbreak_credit, (0, 0))
    
    pygame.display.flip()
    pygame.time.delay(3000)  # Display for 3 seconds

video_clip = VideoFileClip("chitauri.mp4")
video_frame_rate = video_clip.fps
video_frame_duration = 1 / video_frame_rate


def start_level_7(selected_chara):
    global players_healthy, blueskull_healthy, game_started, video_played, show_start_screen, show_instruction_screen,show_level_screen
     
    players_healthy = max_player_health
    blueskull_healthy = max_blueskull_health

    if selected_chara == "IRON WARRIOR":
     hero = Hero(50, screen_height - 100, char_images[selected_chara], laser_img)
    elif selected_chara == "CAPTAIN WILLIE":
     hero = Hero(50, screen_height - 100, char_images[selected_chara], laptopshot_img)
    elif selected_chara == "STORMBREAK":
     hero = Hero(50, screen_height - 100, char_images[selected_chara], thunder_img)
   

    enemy = Titan(screen_length - 150, screen_height - 100, enemy_photo)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not show_start_screen:
                    show_start_screen = True
                elif event.key == pygame.K_SPACE and show_instruction_screen:
                    game_started = True
                    show_instruction_screen = False
                elif event.key == pygame.K_f:  
                    toggle_fullscreen()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    hero.activate_special_power()

        if show_level_screen:
            draw_level_screen()
            show_level_screen = False
            show_start_screen = True
        if show_start_screen:
            draw_start_screen()
            pygame.time.delay(1000)  # Delay for players
            show_start_screen = False
            show_instruction_screen = True

        elif show_instruction_screen:
            draw_instruction_screen()
            pygame.time.delay(1000)  
            show_instruction_screen = False
            game_started=True  

        elif game_started:
            keys = pygame.key.get_pressed()
            hero.move(keys)
            hero.attack(keys)
            hero.update_hitboxes()

            enemy.move()
            enemy.attack()
            enemy.update_hitboxes()

            handle_attacks(hero, enemy)
            handle_bullets(hero, enemy)

            # Draw background and selectedchara
            window.blit(image, (0, 0))  
            hero.draw(window)
            enemy.draw(window)

            # Update health bars
            player_health_bar_width = int((players_healthy / max_player_health) * 200)
            blueskull_health_bar_width = int((blueskull_healthy / max_blueskull_health) * 200)
            pygame.draw.rect(window, RED, (10, 50, player_health_bar_width, 20))
            pygame.draw.rect(window, RED, (screen_length - blueskull_health_bar_width - 10, 50, blueskull_health_bar_width, 20))

            # Display health
            health_text = small_font.render(f"Player Health: {players_healthy}", True, WHITE)
            window.blit(health_text, (10, 30))

            enemy_health_text = small_font.render(f"Titan Health: {blueskull_healthy}", True, WHITE)
            window.blit(enemy_health_text, (screen_length - 200, 30))

            
            window.blit(button_img, button_rect.topleft)

            pygame.display.flip()

            if blueskull_healthy <= 0:
                print("Blueskull is defeated")
                show_credits(selected_chara)
                running = False
            
            if players_healthy <= 0:
                print("You are dead")
                running = False

            clock.tick(60)

    pygame.quit()
    sys.exit()






