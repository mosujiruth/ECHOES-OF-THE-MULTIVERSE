#blood sweat an tears of tarshni
import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sin to Save")

# Background image
bg_image = pygame.image.load('sintosave.jpg')
bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))  

# Player images
player1_img = pygame.image.load('captainwillie.png')
player1_img = pygame.transform.scale(player1_img, (200, 200))  

player2_img = pygame.image.load('sorceress.png')
player2_img = pygame.transform.scale(player2_img, (150, 150)) 

#font colours
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)


#colors
white = (255, 255, 255)
black = (0, 0, 0)

#fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

game_started = False
show_level_screen = True
show_instruction_screen = False
level_display_duration = 2000  # will show for 2 sec
level_start_time = pygame.time.get_ticks()

# Player position
player1_x, player1_y = 20, 350  
player2_x, player2_y = 650, 380  
player1_health = 100
player2_health = 100

# Health bar
def draw_health_bar(health, x, y):
    pygame.draw.rect(screen, white, (x, y, 100, 20))
    pygame.draw.rect(screen, (255, 0, 0), (x, y, health, 20))

#level screen
def draw_level_screen():
    screen_width = 800
    screen_height = 600
    bg_image = pygame.image.load('redevil.jpg')
    bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))
    screen.blit(bg_image, (0, 0))
    level_text = font.render("Level 6", True, blue)
    screen.blit(level_text, (screen_width//2 - level_text.get_width()//2, screen_height//2))
    pygame.display.flip()

#start screen
def draw_start_screen():
    screen.blit(bg_image, (0, 0))  
    title_text = font.render("Sin to Save", True, green)
    start_text = small_font.render("Click ENTER to start", True, green)

    screen.blit(title_text, (screen_width//2 - title_text.get_width()//2, screen_height//3))
    screen.blit(start_text, (screen_width//2 - start_text.get_width()//2, screen_height//2))
    pygame.display.flip()

#story screen
def draw_instruction_screen():
    screen_width = 800
    screen_height = 600
    bg_image = pygame.image.load('extract.jpg')
    bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))
    screen.blit(bg_image, (0, 0))
    instruction_text = small_font.render("Defeat the sorceress to obtain the mind stone from vision", True, green)
    continue_text = small_font.render("Press SPACE to continue", True, green)

    screen.blit(instruction_text, (screen_width//2 - instruction_text.get_width()//2, screen_height//3))
    screen.blit(continue_text, (screen_width//2 - continue_text.get_width()//2, screen_height//2))
    pygame.display.flip()

# Mainloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not show_instruction_screen:
                game_started = False
                show_instruction_screen = True
            elif event.key == pygame.K_SPACE and show_instruction_screen:
                game_started = True
                show_instruction_screen = False

    current_time = pygame.time.get_ticks()
    if show_level_screen:
        draw_level_screen()
        if current_time - level_start_time > level_display_duration:
            show_level_screen = False  
    elif not game_started and not show_instruction_screen:
        draw_start_screen()
    elif show_instruction_screen:
        draw_instruction_screen()
    else:
        #game screen
        screen.blit(bg_image, (0, 0)) 
        screen.blit(player1_img, (player1_x, player1_y))  
        screen.blit(player2_img, (player2_x, player2_y))  

        #health bars
        draw_health_bar(player1_health, 50, 50)
        draw_health_bar(player2_health, 650, 50)

        pygame.display.flip()

