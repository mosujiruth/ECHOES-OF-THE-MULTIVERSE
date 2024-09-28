import pygame
import sys
from moviepy.editor import VideoFileClip
import numpy as np


pygame.init()
pygame.font.init()
pygame.mixer.init()

BLACK = (255, 255, 255)
WHITE = (0, 0, 0)
YELLOW = (255, 255, 0)

# Initialize the screen
screen_length = 600
screen_height = 400
window =pygame.display.set_mode((screen_length, screen_height),pygame.FULLSCREEN)
pygame.display.set_caption("ECHOES OF THE MULTIVERSE")
font = pygame.font.SysFont('Comic Sans', 30)

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

enemy_photo = pygame.image.load("blueskull.png").convert_alpha()
enemy_photo = pygame.transform.scale(enemy_photo, (100, 100))

image=pygame.image.load("vormir.png")
image=pygame.transform.scale(image,(screen_length,screen_height))

button_click_sound = pygame.mixer.Sound("Bitter.wav")

def play_button_click_sound():
    button_click_sound.play()

char_images = {
    "IRON WARRIOR": char_1,
    "CAPTAIN WILLIE": char_2,
    "STORMBREAK": char_3
}

button_width = 300
button_height = 60
  
phew_phew=pygame.mixer.Sound("laser-gun.mp3")  
# Function to display text inside a button
def draw_button(text, font, color, rect):
    pygame.draw.rect(window, WHITE, rect)
    text_surface = font.render(text, True, color)
    window.blit(text_surface, (rect.x + (rect.width - text_surface.get_width()) // 2,
                               rect.y + (rect.height - text_surface.get_height()) // 2))
    
players_healthy = 150
blueskull_healthy = 150

enemy_bullet_cooldown = 1000
enemy_bullets = []


def phew_phew_key():
    phew_phew.play()
# Hero class
class Heroes:
    def __init__(self, image, bullet_img, bullet_speed, typesof_bullet):
        self.image = image
        self.bullet_img = bullet_img
        self.typesof_bullet = typesof_bullet
        self.bullet_speed = bullet_speed

    def firing_bullettypes(self, x, y):
        return [Bullet(self.bullet_img, x + 90, y + 40  , self.bullet_speed)]

    def draw(self, window, x, y):
        window.blit(self.image, (x, y))

# Bullet class
class Bullet:
    def __init__(self, image, x, y, speed):
        self.image = image
        self.x = x
        self.y = y
        self.speed = speed

    def move(self):
        self.x += self.speed

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

# Blueskull class
class Blueskull:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.direction = 1
        self.speed = 0.25
        self.last_shot_time = pygame.time.get_ticks()
    def move(self):
        self.y += self.direction * self.speed
        if self.y <= 50:
            self.direction = 1
        elif self.y >= screen_height - 150:
            self.direction = -1
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > enemy_bullet_cooldown:
            enemy_bullets.append(BlueskullBullet(laser_img, self.x, self.y + 40, 3))  
            self.last_shot_time = current_time

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

class BlueskullBullet(Bullet):
    def move(self):
        self.x -= self.speed

ironwarrior = Heroes(char_1, laser_img, 3, "laser")
captainwillie = Heroes(char_2, laptopshot_img, 3, "laptopshot")
stormbreak = Heroes(char_3, thunder_img, 3, "thunder")

def toggle_fullscreen():
    global fullscreen, window
    if fullscreen:
        window = pygame.display.set_mode((screen_length, screen_height), pygame.RESIZABLE | pygame.SCALED)
        fullscreen = False
    else:
        window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.SCALED)
        fullscreen = True

bullets = []
maximum_bullet = 12
bullet_cooldowntime = 300
last_shot_timimg = pygame.time.get_ticks()
players_x, players_y = 0, screen_height - 120

blueenemy = Blueskull(enemy_photo, 450, 250)
def display_message(message, windows):
    text_surface = font.render(message, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(screen_length // 2, screen_height // 2))
    windows.blit(text_surface, text_rect)
    pygame.display.flip()


def sacrifice_part(selected_chara):
    running= True
    correct_sacrifice= None
    reality_stone=pygame.image.load("soul stone.png")
    reality_stone=pygame.transform.scale(reality_stone,(screen_length,screen_height))

    if selected_chara == "IRON WARRIOR":
        option1= "RODY"
        option2= "NATASHA"
        correct_sacrifice = option2

    elif selected_chara == "CAPTAIN WILLIE":
        option1= "BUCKY"
        option2= "SAGA"
        correct_sacrifice = option2

    elif selected_chara == "STORMBREAK":
        option1= "LOKI"
        option2= "ROCKET"
        correct_sacrifice = option2

    players_choice= None

    button1_rect = pygame.Rect(screen_length // 2 - button_width // 2, 150, button_width, button_height)
    button2_rect = pygame.Rect(screen_length // 2 - button_width // 2, 250, button_width, button_height)

    while running:
        window.blit(image, (0, 0))  

        
        draw_button(f"Sacrifice {option1}", font, BLACK, button1_rect)
        draw_button(f"Sacrifice {option2}", font, BLACK, button2_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                
                if button1_rect.collidepoint(mouse_pos):
                    button_click_sound.play()
                    players_choice = option1
                elif button2_rect.collidepoint(mouse_pos):
                    button_click_sound.play()
                    players_choice = option2

                
                if players_choice == correct_sacrifice:
                    window.blit(reality_stone, (0, 0)) 
                    display_message("YOU HAVE RECEIVED THE STONE",window)
                    pygame.display.update()
                    pygame.time.delay(3000)
                    running = False
                    try:
                      import level_5
                      print("Imported level_5 successfully")
                      level_5.start_level_5(selected_chara)
                    except ImportError as e:
                         print(f"Error importing level_5: {e}")
                    except Exception as e:
       
                          print(f"An error occurred: {e}")
                else:
                    window.fill(BLACK)
                    display_message("Try again!", window)
                    pygame.display.update()
                    pygame.time.delay(2000)  # Pause before resetting options
                    players_choice = None  

    pygame.quit()
    sys.exit()

start_screen=0
instruction_screen=1
video_playing=2
game_played=3
current_state=start_screen


def draw_level_screen():
    level_bgg = pygame.image.load('vormir.1.png')  
    level_bgg = pygame.transform.scale(level_bgg, (screen_length, screen_height))
    window.blit(level_bgg, (0, 0))
    level_text = font.render("Level 4", True, YELLOW)
    window.blit(level_text, (screen_length//2 - level_text.get_width()//2, screen_height//2))
    pygame.display.flip()
 
def draw_instruction_screen():
    instruction_bgg = pygame.image.load("vormir.1.png")
    instruction_bgg=pygame.transform.scale(instruction_bgg,(screen_length,screen_height))
    small_font = pygame.font.Font(None, 24)  
    window.blit(instruction_bgg, (0, 0))
    instruction_text = small_font.render("Defeat Blueskull to obtain the soul stone", True, YELLOW)
    continue_text1 = small_font.render("left key(left),Right key(right),up key(up),down key(down),space key(shoot)", True, YELLOW)
    continue_text2 = small_font.render("Press SPACE to continue", True, YELLOW)
    window.blit(instruction_text, (screen_length//2 - instruction_text.get_width()//2, screen_height//4))
    window.blit(continue_text1, (screen_length//2 - continue_text1.get_width()//2, screen_height//3.5))
    window.blit(continue_text2, (screen_length//2 - continue_text2.get_width()//2, screen_height//2.5))
    pygame.display.flip()

def play_video():
    global current_state
    video_placement = "vormir-space.mp4"
    clip = VideoFileClip(video_placement)
    for frame in clip.iter_frames(fps=30):
        frame_surface = pygame.surfarray.make_surface(np.array(frame))
        frame_surface = pygame.transform.scale(frame_surface, (screen_length, screen_height))
        window.blit(frame_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(int(1000 / clip.fps))
    
    current_state = game_played 

def draw_end_screen(result):
    window.fill(BLACK)
    end_text = font.render(result, True, YELLOW)
    window.blit(end_text, (screen_length//2 - end_text.get_width()//2, screen_height//3))
    replay_text = font.render("Press R to replay or ESC to quit", True, YELLOW)
    window.blit(replay_text, (screen_length//2 - replay_text.get_width()//2, screen_height//2))
    pygame.display.flip()

def start_level_4(selected_chara):
    global last_shot_timimg, bullets, players_healthy, blueskull_healthy, enemy_bullets, current_state,show_end_screen

    hero = None
    if selected_chara == "IRON WARRIOR":
        hero = ironwarrior
    elif selected_chara == "CAPTAIN WILLIE":
        hero = captainwillie
    elif selected_chara == "STORMBREAK":
        hero = stormbreak
    else:
        print("Invalid character selected!")
        return
    
    players_x, players_y = 0, screen_height - 120
    players_speed = 5 
    running = True
    show_end_screen = False
    end_screen_result = ""
    
    while running:
        current_timimg = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
               
                if event.key == pygame.K_UP:
                    players_y -= players_speed
                if event.key == pygame.K_DOWN:
                    players_y += players_speed
                if event.key == pygame.K_SPACE:
                    phew_phew.play()
                    if current_timimg - last_shot_timimg > bullet_cooldowntime:
                        if len(bullets) < maximum_bullet:
                            new_bullety = hero.firing_bullettypes(players_x, players_y)
                            bullets.extend(new_bullety)
                            last_shot_timimg = current_timimg
                if event.key == pygame.K_SPACE:
                    if current_state == start_screen:
                        current_state = instruction_screen 
                    elif current_state == instruction_screen:
                        current_state = video_playing  
                    elif current_state == video_playing:
                        current_state = game_played  
                 
                if event.key == pygame.K_r:
                # Reset all variables
                 players_healthy = 150
                 blueskull_healthy = 150
                 bullets.clear()
                 enemy_bullets.clear()
                 current_state = start_screen  # Reset state to start screen
                 start_level_4(selected_chara)        
        
        if current_state == start_screen:
            draw_level_screen() 
        elif current_state == instruction_screen:
            draw_instruction_screen() 
        elif current_state == video_playing:
            play_video()  
        elif current_state == game_played:
            
            window.blit(image, (0, 0))  
            
            
            for bullet in bullets[:]:
                bullet.move()
                if bullet.x > screen_length:
                    bullets.remove(bullet)
                elif blueenemy.x < bullet.x < blueenemy.x + 100 and blueenemy.y < bullet.y < blueenemy.y + 100:
                    bullets.remove(bullet)
                    blueskull_healthy -= 10

            
            blueenemy.shoot()
            for bullet in enemy_bullets[:]:
                bullet.move()
                if bullet.x < 0:
                    enemy_bullets.remove(bullet)
                elif players_x < bullet.x < players_x + 100 and players_y < bullet.y < players_y + 100:
                    enemy_bullets.remove(bullet)
                    players_healthy -= 10

            
            pygame.draw.rect(window, YELLOW, (10, 10, players_healthy, 20))
            pygame.draw.rect(window, YELLOW, (screen_length - blueskull_healthy - 10, 10, blueskull_healthy, 20))

            
            hero.draw(window, players_x, players_y)
            blueenemy.move()
            blueenemy.draw(window)
            for bullet in bullets:
                bullet.draw(window)
            for bullet in enemy_bullets:
                bullet.draw(window)

        pygame.display.update()

       
        if blueskull_healthy <= 0:
            print("Blueskull is defeated")
            running = False
            sacrifice_part(selected_chara)
        if players_healthy <= 0:
            print("You are dead")
            show_end_screen=True
            end_screen_result = "You are dead!"
            current_state = "end_screen"
        elif show_end_screen: 
            draw_end_screen(end_screen_result)  


    pygame.quit()
    sys.exit()
