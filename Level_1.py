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

# Create the window
Window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Level 1: Obtaining Gauntlet")

# Choose font type
font = pygame.font.SysFont('Comic Sans MS', 11)

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

# Displaying and scaling Captain willie shield
Captain_Willie_Shield = pygame.image.load("Captain_Willie_Shield.png").convert_alpha()
Captain_Willie_Shield = pygame.transform.scale(Captain_Willie_Shield, (100, 100))

# Try loading the EagleEye bow image, handle errors if it fails
try:
    EagleEye_bow = pygame.image.load("EagleEye_bow.png").convert_alpha()
    EagleEye_bow = pygame.transform.scale(EagleEye_bow, (100, 100))
except pygame.error as e:
    print(f"Error loading EagleEye_bow image: {e}")
    EagleEye_bow = None  # Prevent crashes by setting to None if loading fails

# Create Button class for options
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

# Use this for clicking on heroes
character_1 = Button(75, 110, character_1_img)
character_2 = Button(230, 110, character_2_img)
character_3 = Button(380, 110, character_3_img)

# Game states
character_selection = 0  # Initial game state for character selection
level_1_dialogue = 1  # Game state for dialogue
level_1_options = 2  # Game state for options
dialogue_state = 3  # Game state for displaying dialogue after correct option
current_state = character_selection  # Set the current state to character selection
selected_hero = None  # Variable stores selected hero

# Dialogue index
dialogue_index = 0
dialogue_displayed = False

# Option selection
options = []  # This will hold Button objects for each option
correct_option_index = 0  # Placeholder for the correct option
options_displayed = False  # Track if options have been displayed

# Function to draw dialogue bubble
def draw_bubble(text, position):
    padding = 8
    text_surface = font.render(text, True, Black)
    bubble_width = text_surface.get_width() + 2 * padding
    bubble_height = text_surface.get_height() + 2 * padding
    bubble = pygame.Surface((bubble_width, bubble_height))
    bubble.fill(White)
    pygame.draw.rect(bubble, Black, bubble.get_rect(), 2)  # Bubble border
    bubble.blit(text_surface, (padding, padding))
    Window.blit(bubble, position)

# Function to create option buttons
def create_options(option_texts, correct_index, start_x=200, start_y=200, gap=40):
    global options, correct_option_index, options_displayed
    options = []
    correct_option_index = correct_index
    options_displayed = True
    for i, text in enumerate(option_texts):
        button = Button(start_x, start_y + i * gap, text=text, width=250, height=30)
        options.append(button)

# Main game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If quit button clicked
            running = False  # Exit the loop and quits the game
        elif event.type == pygame.MOUSEBUTTONDOWN and current_state == character_selection:
            if character_1.is_clicked(event.pos):
                selected_hero = "Iron Warrior"  # set selected hero to Iron Warrior
                current_state = level_1_dialogue  # move to dialogue state
            elif character_2.is_clicked(event.pos): 
                selected_hero = "Captain Willie"
                current_state = level_1_dialogue
            elif character_3.is_clicked(event.pos):
                selected_hero = "Stormbreak"
                current_state = level_1_dialogue
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if current_state == level_1_dialogue:
                # After Enter, move to options state
                if selected_hero == "Iron Warrior":
                    create_options(["Use Captain Willie's Shield", "Use EagleEye's Bow"], 0)
                elif selected_hero == "Captain Willie":
                    create_options(["Iron Warrior", "Wizard Supreme"], 0)
                elif selected_hero == "Stormbreak":
                    create_options(["Iron Warrior", "Blue Skull"], 0)
                current_state = level_1_options

            elif current_state == dialogue_state:
                dialogue_index += 1
                
                # Ending game after the last dialogue for each hero
                if selected_hero == "Captain Willie" and dialogue_index == 6:
                    running = False  # End the game after the last dialogue for Captain Willie
                elif selected_hero == "Stormbreak" and dialogue_index == 6:
                    running = False  # End the game after the last dialogue for Stormbreak
                elif selected_hero == "Iron Warrior" and dialogue_index == 1:
                    running = False  # End the game after the last dialogue for Iron Warrior

        elif event.type == pygame.MOUSEBUTTONDOWN and current_state == level_1_options:
            for i, option in enumerate(options):
                if option.is_clicked(event.pos):
                    if i == correct_option_index:
                        dialogue_index = 0
                        current_state = dialogue_state  # Move to the dialogue state
                    else:
                        running = False  # End the game if the wrong option is chosen

    Window.blit(image, (0, 0))  # Draw background image
    if current_state == character_selection:
        character_1.draw(Window)  # Draw Iron Warrior
        character_2.draw(Window)  # Draw Captain Willie
        character_3.draw(Window)  # Draw Stormbreak

    elif current_state == level_1_dialogue:
        # Draw selected hero and dialogue
        if selected_hero == "Iron Warrior":
            character_1.draw(Window)
            draw_bubble("Which item should we use to make a gauntlet?", (character_1.rect.x, character_1.rect.y - 40))
            Window.blit(Captain_Willie_Shield, (character_1.rect.x + 320, character_1.rect.y + 50))  # Draw Captain Willie's shield
            if EagleEye_bow:  # Check if the bow is loaded correctly
                Window.blit(EagleEye_bow, (character_1.rect.x + 200, character_1.rect.y + 50))  # Draw EagleEye's bow beside the shield
        elif selected_hero == "Captain Willie":
            character_2.draw(Window)
            draw_bubble("Who should we ask for help?", (character_2.rect.x, character_2.rect.y - 40))
        elif selected_hero == "Stormbreak":
            character_3.draw(Window)
            draw_bubble("Who is able to make me a gauntlet?", (character_3.rect.x, character_3.rect.y - 40))

    elif current_state == level_1_options:
        for option in options:
            option.draw(Window)

    elif current_state == dialogue_state:
        if selected_hero == "Iron Warrior":
            if dialogue_index < 1:
                draw_bubble("Let's begin melting this shield.", (character_1.rect.x, character_1.rect.y - 40))
                Window.blit(Captain_Willie_Shield, (character_1.rect.x + 200, character_1.rect.y + 50))
                character_1.draw(Window)  # Draw Iron Warrior
        elif selected_hero == "Captain Willie":
            character_2.draw(Window)
            character_1.draw(Window)
            if dialogue_index < 6:
                if dialogue_index % 2 == 0:
                    draw_bubble(["Hey Iron Warrior, can you do me a help?",
                                 "I need a gauntlet to defeat Thanos.",
                                 "Thanks Iron Warrior"][dialogue_index // 2],                             
                                (character_2.rect.x, character_2.rect.y - 40))
                else:
                    draw_bubble(["What can I help you with, Cap?",
                                 "Okay Cap, I'll do the gauntlet ASAP",
                                 "Don't mention it, Cap"][dialogue_index // 2],                               
                                (character_1.rect.x, character_1.rect.y - 40))

        elif selected_hero == "Stormbreak":
            character_3.draw(Window)
            character_1.draw(Window)
            if dialogue_index < 6:
                if dialogue_index % 2 == 0:
                    draw_bubble(["Hey Iron Warrior, I need your help.",
                                 "I need a gauntlet to destroy Thanos.",
                                 "Alright then Iron Warrior, see you soon"][dialogue_index // 2], 
                                (character_3.rect.x, character_3.rect.y - 40))
                else:
                    draw_bubble(["Yo Stormbreak, what can I help you with?",
                                 "Sure thing, will get it done soon",
                                 "Okay Stormbreak, see ya"][dialogue_index // 2], 
                                (character_1.rect.x, character_1.rect.y - 40))

    pygame.display.update()

# Quit pygame and exit program
pygame.quit()
sys.exit()
