import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sin to Save")

#background image
bg_image = pygame.image.load('sintosave.jpg')
bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))  # Resize image to fit screen

#player images
player1_img = pygame.image.load('captainwillie.png')
player1_img = pygame.transform.scale(player1_img, (200, 200))  

player2_img = pygame.image.load('BLUE SKULL.png')
player2_img = pygame.transform.scale(player2_img, (150, 150)) 

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set up fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

game_started = False
show_level_screen = True
level_display_duration = 2000  # will show 2 sec
level_start_time = pygame.time.get_ticks()

#Playerposition
player1_x, player1_y = 20, 350  
player2_x, player2_y = 650, 380  
player1_health = 100
player2_health = 100

#health bar
def draw_health_bar(health, x, y):
    pygame.draw.rect(screen, white, (x, y, 100, 20))
    pygame.draw.rect(screen,  (255, 0, 0), (x, y, health, 20))

# Draw opening screen
def draw_level_screen():
    screen_width = 800
    screen_height = 600
    bg_image = pygame.image.load('redevil.jpg')
    bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))
    screen.blit(bg_image, (0, 0))
    level_text = font.render("Level 6", True, white)
    screen.blit(level_text, (screen_width//2 - level_text.get_width()//2, screen_height//2))
    pygame.display.flip()

# Draw second screen
def draw_start_screen():
    screen.blit(bg_image, (0, 0))  
    title_text = font.render("Sin to Save", True, white)
    start_text = small_font.render("Click ENTER to start", True, white)

    screen.blit(title_text, (screen_width//2 - title_text.get_width()//2, screen_height//3))
    screen.blit(start_text, (screen_width//2 - start_text.get_width()//2, screen_height//2))
    pygame.display.flip()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game_started = True

    current_time = pygame.time.get_ticks()
    if show_level_screen:
        draw_level_screen()
        if current_time - level_start_time > level_display_duration:
            show_level_screen = False  # Stop showing the "Level 6" screen after the duration
    elif not game_started:
        draw_start_screen()
    else:
        # Drawing the game screen
        screen.blit(bg_image, (0, 0)) 
        screen.blit(player1_img, (player1_x, player1_y))  
        screen.blit(player2_img, (player2_x, player2_y))  

        # Draw health bars
        draw_health_bar(player1_health, 50, 50)
        draw_health_bar(player2_health, 650, 50)

        pygame.display.flip()
