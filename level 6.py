#blood sweat and tears of tarshni
import pygame
import sys
# Initialize Pygame
pygame.init()

#Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sin to Save")

# Load background image
bg_image = pygame.image.load('sintosave.jpg')
bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))  # Resize image to fit screen

# Define colors
white = (0, 255, 0)
black = (0, 0, 0)

# Set up fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Game state
game_started = False
show_level_screen = True
level_display_duration = 2000  #will show 2 sec
level_start_time = pygame.time.get_ticks()  

def draw_level_screen():
    screen_width = 800
    screen_height = 600
    bg_image = pygame.image.load('redevil.jpg')
    bg_image=pygame.transform.scale(bg_image,(screen_width,screen_height))
    screen.blit(bg_image, (0, 0)) 
    level_text = font.render("Level 6", True, white)
    screen.blit(level_text, (screen_width//2 - level_text.get_width()//2, screen_height//2))
    pygame.display.flip()

def draw_start_screen():
    screen.blit(bg_image, (0, 0))  # Draw the background image
    title_text = font.render("Sin to Save", True, white)
    start_text = small_font.render("Press ENTER to start", True, white)

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
        # Here you would start the actual game
        screen.blit(bg_image, (0, 0))  # Draw the background pic for the game
        font = pygame.font.Font(None, 40)
        game_text = font.render("To obtain the Mind stone defeat wanda to get to vision", True, white)
        screen.blit(game_text, (screen_width//2 - game_text.get_width()//2, screen_height//2))
        pygame.display.flip()
