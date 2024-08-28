import pygame
import sys

# Initialize pygame
pygame.init()
pygame.font.init()

# Set screen width and height
screen_width = 600
screen_height = 400

# Define colors
White = (255, 255, 255)
Black = (0, 0, 0)

# Create the window
Window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Level 1: Obtaining Gauntlet")

# Choose font type
font = pygame.font.SysFont('Comic Sans MS', 20)

# Displaying Stark Office Background
image = pygame.image.load("Stark_Lab.png")
image = pygame.transform.scale(image, (screen_width, screen_height))

# Displaying characters images
character_1_img = pygame.image.load("iron_warrior.png").convert_alpha()
character_2_img = pygame.image.load('captainwillie.png').convert_alpha()
character_3_img = pygame.image.load("stormbreak.png").convert_alpha()

# Scaling heroes
character_1_img = pygame.transform.scale(character_1_img, (180, 170))
character_2_img = pygame.transform.scale(character_2_img, (190, 170))
character_3_img = pygame.transform.scale(character_3_img, (110, 170))

# Displaying and scaling gauntlet
gauntlet = pygame.image.load("Gauntlet.webp").convert_alpha()
gauntlet = pygame.transform.scale(gauntlet, (100, 100))

class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
    
    def is_clicked(self, position):
        return self.rect.collidepoint(position)

#Use this for clicking on heroes
character_1 = Button(75, 110, character_1_img)
character_2 = Button(230, 110, character_2_img)
character_3 = Button(380, 110, character_3_img)

# Game states
character_selection = 0 # Initial game state for character selection
level_1 = 1 # Game state for level 1
current_state = character_selection # Set the current state to character selection
selected_hero = None # Variable stores selected hero

# Set up dialogue based on selected hero
if selected_hero == "Iron Warrior":
    dialogue = [
        "Iron Warrior: Hmm, I have Cap's shield.",
        "Iron Warrior: I can melt this and make a gauntlet."
    ]
elif selected_hero == "Captain Willie":
    dialogue = [
        "Captain Willie: Iron Warrior, we need your help.",
        "Iron Warrior: Sure, I can melt my shield to make a gauntlet."
    ]
elif selected_hero == "Stormbreak":
    dialogue = [
        "Stormbreak: Iron Warrior, we need your help.",
        "Iron Warrior: Sure, I can melt Cap's shield to make a gauntlet."
    ]

# Dialogue index and gauntlet appearance tracker
dialogue_index = 0
gauntlet_appeared = False # Intialize gauntlet appearance to False

# Main game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # If quit button clicked 
            running = False # Exit the loop and quits the game
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if character_1.is_clicked(event.pos):
                selected_hero = "Iron Warrior" # set selected hero to Iron Warrior
                current_state = level_1 # change state to level 1 
            elif character_2.is_clicked(event.pos): 
                selected_hero = "Captain Willie"
                current_state = level_1
            elif character_3.is_clicked(event.pos):
                selected_hero = "Stormbreak"
                current_state = level_1

    Window.blit(image, (0, 0)) # Draw background image
    if current_state == character_selection:
        character_1.draw(Window) # Draw Iron Warrior
        character_2.draw(Window)
        character_3.draw(Window)
    elif current_state == level_1:
        if selected_hero == "Iron Warrior": # If Iron Warrior is selected
            character_1.draw(Window) # Draw Iron Warrior
        elif selected_hero == "Captain Willie":
            character_2.draw(Window) 
        elif selected_hero == "Stormbreak":
            character_3.draw(Window)
        
        character_1.draw(Window) # always display iron warrior in the whole level 1

        if selected_hero == "Iron Warrior": # if iron warrior is selected
            pass # no extra characters needed
        elif selected_hero == "Captain Willie": # if iron warrior is selected
            character_2.draw(Window) # draw captain willie again
        elif selected_hero == "Stormbreak":
            character_3.draw(Window)

    pygame.display.flip() # Update the display

pygame.quit() 
sys.exit()


