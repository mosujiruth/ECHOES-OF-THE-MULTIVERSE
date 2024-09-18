<<<<<<< HEAD

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
Red = (255, 0, 0)

# Create window
Window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Level 2: Convince Sorcerer Supreme")

# Choose font type
font = pygame.font.SysFont('Comic Sans MS', 20)

# Displaying Stark Office Background
image = pygame.image.load("Strange_Office.png")
image = pygame.transform.scale(image, (screen_width, screen_height))

# Displaying characters images
character_1_img = pygame.image.load("iron_warrior.png").convert_alpha()
character_2_img = pygame.image.load('captainwillie.png').convert_alpha()
character_3_img = pygame.image.load("stormbreak.png").convert_alpha()

# Scaling heroes
character_1_img = pygame.transform.scale(character_1_img, (170, 200))
character_2_img = pygame.transform.scale(character_2_img, (180, 200))
character_3_img = pygame.transform.scale(character_3_img, (110, 200))

# New character
character_4_img = pygame.image.load("WizardSupreme.png").convert_alpha()
character_4_img = pygame.transform.scale(character_4_img,(230, 200))

class Button:
    def __init__(self, x, y, image=None, text="", width=200, height=30):
        self.image = image
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = Black
        if image:
            self.rect = self.image.get_rect(topleft=(x, y))
    
    def draw(self, surface):
        if self.image:
            surface.blit(self.image, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(surface, self.color, self.rect)
            text_surface = font.render(self.text, True, White)
            surface.blit(text_surface, (self.rect.x + 10, self.rect.y + 5))
    
    def is_clicked(self, position):
        return self.rect.collidepoint(position)

# Use this to click on heroes
character_1 = Button(70, 130, character_1_img)
character_2 = Button(250, 130, character_2_img)
character_3 = Button(450, 130, character_3_img)

# Game states
character_selection = 0  # Initial game state for character selection
level_2 = 1  # Game state for level 2
current_state = character_selection  # Set the current state to character selection
selected_hero_img = None  # Variable stores selected hero


#Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If quit button clicked
            running = False  # Exit the loop and quits the game
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == character_selection:
                if character_1.is_clicked(event.pos):
                    selected_hero_img = "Iron Warrior"  # set selected hero to Iron Warrior
                    current_state = level_2  # change state to level 2

                elif character_2.is_clicked(event.pos): 
                    selected_hero_img = "Captain Willie"
                    current_state = level_2
                
                elif character_3.is_clicked(event.pos):
                    selected_hero_img = "Stormbreak"
                    current_state = level_2
                
    Window.blit(image, (0, 0))  # Draw background image

    if current_state == character_selection:
        character_1.draw(Window)  # Draw Iron Warrior
        character_2.draw(Window)
        character_3.draw(Window)
        
    elif selected_hero_img == "Iron Warrior":
        Window.blit(character_1_img, (100, 130)) #Draw iron warrior
        Window.blit(character_4_img, (300,130))  #Draw sorccerer supreme

    elif selected_hero_img == "Captain Willie":
        Window.blit(character_2_img, (100, 130))
        Window.blit(character_4_img, (300,130))

    elif selected_hero_img == "Stormbreak":
        Window.blit(character_3_img, (100, 130))
        Window.blit(character_4_img, (300,130))
    
    pygame.display.flip()  # Update the display

pygame.quit()
sys.exit()

=======

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
Red = (255, 0, 0)

# Create window
Window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Level 2: Convince Sorcerer Supreme")

# Choose font type
font = pygame.font.SysFont('Comic Sans MS', 20)

# Displaying Stark Office Background
image = pygame.image.load("Strange_Office.png")
image = pygame.transform.scale(image, (screen_width, screen_height))

# Displaying characters images
character_1_img = pygame.image.load("iron_warrior.png").convert_alpha()
character_2_img = pygame.image.load('captainwillie.png').convert_alpha()
character_3_img = pygame.image.load("stormbreak.png").convert_alpha()

# Scaling heroes
character_1_img = pygame.transform.scale(character_1_img, (170, 200))
character_2_img = pygame.transform.scale(character_2_img, (180, 200))
character_3_img = pygame.transform.scale(character_3_img, (110, 200))

# New character
character_4_img = pygame.image.load("sorccerersupreme.png").convert_alpha()
character_4_img = pygame.transform.scale(character_4_img,(170, 200))

class Button:
    def __init__(self, x, y, image=None, text="", width=200, height=30):
        self.image = image
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = Black
        if image:
            self.rect = self.image.get_rect(topleft=(x, y))
    
    def draw(self, surface):
        if self.image:
            surface.blit(self.image, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(surface, self.color, self.rect)
            text_surface = font.render(self.text, True, White)
            surface.blit(text_surface, (self.rect.x + 10, self.rect.y + 5))
    
    def is_clicked(self, position):
        return self.rect.collidepoint(position)

# Use this to click on heroes
character_1 = Button(70, 130, character_1_img)
character_2 = Button(250, 130, character_2_img)
character_3 = Button(450, 130, character_3_img)

# Game states
character_selection = 0  # Initial game state for character selection
level_2 = 1  # Game state for level 2
current_state = character_selection  # Set the current state to character selection
selected_hero_img = None  # Variable stores selected hero


#Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If quit button clicked
            running = False  # Exit the loop and quits the game
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == character_selection:
                if character_1.is_clicked(event.pos):
                    selected_hero_img = "Iron Warrior"  # set selected hero to Iron Warrior
                    current_state = level_2  # change state to level 2

                elif character_2.is_clicked(event.pos): 
                    selected_hero_img = "Captain Willie"
                    current_state = level_2
                
                elif character_3.is_clicked(event.pos):
                    selected_hero_img = "Stormbreak"
                    current_state = level_2
                
    Window.blit(image, (0, 0))  # Draw background image

    if current_state == character_selection:
        character_1.draw(Window)  # Draw Iron Warrior
        character_2.draw(Window)
        character_3.draw(Window)
        
    elif selected_hero_img == "Iron Warrior":
        Window.blit(character_1_img, (100, 130)) #Draw iron warrior
        Window.blit(character_4_img, (300,130))  #Draw sorccerer supreme

    elif selected_hero_img == "Captain Willie":
        Window.blit(character_2_img, (100, 130))
        Window.blit(character_4_img, (300,130))

    elif selected_hero_img == "Stormbreak":
        Window.blit(character_3_img, (100, 130))
        Window.blit(character_4_img, (300,130))
    
    pygame.display.flip()  # Update the display

pygame.quit()
sys.exit()

>>>>>>> 28a80e94fdbd0328f42a2b02eccc8f5195c3a5a0
