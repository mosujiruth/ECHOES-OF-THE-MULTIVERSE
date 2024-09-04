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

# Displaying and scaling Captain willie shield
Captain_Willie_Shield = pygame.image.load("Captain_Willie_Shield.png").convert_alpha()
Captain_Willie_Shield = pygame.transform.scale(Captain_Willie_Shield, (100, 100))

# Displaying and scaling gauntlet
gauntlet = pygame.image.load("Gauntlet.png").convert_alpha()
gauntlet = pygame.transform.scale(gauntlet, (100, 100))

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
level_1 = 1  # Game state for level 1
current_state = character_selection  # Set the current state to character selection
selected_hero = None  # Variable stores selected hero

# Dialogue index and gauntlet appearance tracker
dialogue_index = 0
Captain_Willie_Shield_appeared = False
gauntlet_appeared = False  # Initialize gauntlet appearance to False

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
def create_options(option_texts, correct_index, start_x=20, start_y=300, gap=40):
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == character_selection:
                if character_1.is_clicked(event.pos):
                    selected_hero = "Iron Warrior"  # set selected hero to Iron Warrior
                    current_state = level_1  # change state to level 1
                    dialogue_index = 0
                    Captain_Willie_Shield_appeared = False
                    gauntlet_appeared = False
                    create_options(["Melt the shield", "Leave the shield"], 0)
                elif character_2.is_clicked(event.pos): 
                    selected_hero = "Captain Willie"
                    current_state = level_1
                    dialogue_index = 0
                    create_options(["Ask for help", "Fight alone"], 0)
                elif character_3.is_clicked(event.pos):
                    selected_hero = "Stormbreak"
                    current_state = level_1
                    dialogue_index = 0
                    create_options(["Ask for a gauntlet", "Use hammer"], 0)
            elif current_state == level_1:
                if options_displayed:
                    for i, option in enumerate(options):
                        if option.is_clicked(event.pos):
                            if i == correct_option_index:
                                options_displayed = False  # Hide options after correct option
                                options = []  # Clear options
                                dialogue_index += 1
                                if selected_hero == "Captain Willie" and dialogue_index >= 6:
                                    dialogue_index = 5  # Prevent going beyond last dialogue
                                elif selected_hero == "Iron Warrior" and dialogue_index >= 3:
                                    dialogue_index = 2  # Prevent going beyond last dialogue
                                # Debug statement to check if dialogue_index is updated correctly
                                print(f"Option selected, new dialogue_index: {dialogue_index}")
                            else:
                                pygame.quit()
                                sys.exit()
    
    Window.blit(image, (0, 0))  # Draw background image
    if current_state == character_selection:
        character_1.draw(Window)  # Draw Iron Warrior
        character_2.draw(Window)
        character_3.draw(Window)
    elif current_state == level_1:
        if selected_hero == "Iron Warrior":
            character_1.draw(Window)  # Draw Iron Warrior
            if dialogue_index < 3:
                draw_bubble(["Hmm, how do I make a gauntlet?",
                             "Oh wow, Captain Willie left his shield here.",
                             "I can melt this and make me a gauntlet."][dialogue_index],
                            (character_1.rect.x, character_1.rect.y - 40))
            if dialogue_index == 1:  # Show shield after Iron Warrior mentions it
                Window.blit(Captain_Willie_Shield, (character_1.rect.x + 200, character_1.rect.y + 50))
                Captain_Willie_Shield_appeared = True

            if dialogue_index == 2 and not gauntlet_appeared:  # Show gauntlet after the shield
                Window.blit(gauntlet, (character_1.rect.x + 300, character_1.rect.y + 50))
                gauntlet_appeared = True

        elif selected_hero == "Captain Willie":
            character_2.draw(Window)
            character_1.draw(Window)
            if dialogue_index < 8:
                if dialogue_index % 2 == 0:
                    draw_bubble(["Hey Iron Warrior, can you do me a help?",
                                 "I need a gauntlet for myself so I can send Thanos and his troops back from where they came.",
                                 "Well, if you don't help me", 
                                 "Thanos is gonna snap his fingers and wipe half the population.",
                                 "But if you help me, then there is a chance we can win the war"][dialogue_index // 2], 
                                (character_2.rect.x, character_2.rect.y - 40))
                else:
                    draw_bubble(["What can I help you with, Cap?",
                                 "Sure I can help you, but what do I get in return?",
                                 "Okay, Cap. I will help you for the sake of saving my daughter."][dialogue_index // 2], 
                                (character_1.rect.x, character_1.rect.y - 40))

        elif selected_hero == "Stormbreak": 
            character_3.draw(Window)
            character_1.draw(Window)
            if dialogue_index < 6:
                if dialogue_index % 2 == 0:
                    draw_bubble(["Hey Iron Warrior, I need your help.",
                                 "I need you to make me a gauntlet to kill Thanos and his troops.",
                                 "Well if you help me then we can save the world and our family."][dialogue_index // 2], 
                                (character_3.rect.x, character_3.rect.y - 40))
                else:
                    draw_bubble(["Yo Stormbreak, what can I help you with?",
                                 "Sure thing Thor, but what is the reward for helping you?",
                                 "Ahhh yea I kinda forget we are superheroes and yea I'll do it to save the world."][dialogue_index // 2], 
                                (character_1.rect.x, character_1.rect.y - 40))

        if options_displayed:
            for option in options:
                option.draw(Window)

    pygame.display.flip()  # Update the display

pygame.quit()
sys.exit()
