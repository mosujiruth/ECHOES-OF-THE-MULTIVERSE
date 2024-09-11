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
font = pygame.font.SysFont('Comic Sans MS', 15)

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
negotiation_state = 1  # Game state for negotiation
question_state = 2  # Game state for question
dialogue_state = 3  # State for general dialogues
current_state = character_selection  # Set the current state to character selection
selected_hero_img = None  # Variable stores selected hero

# Dialogue index for negotiation
dialogue_index = 0
question_index = 0

# Negotiation dialogues
dialogues = {
    "Iron Warrior": [
        "Iron Warrior: I need the stone to stop Thanos.",
        "Sorcerer Supreme: And why should I trust you with it?",
        "Iron Warrior: I'm the only one who can use it properly."
    ],
    "Captain Willie": [
        "Captain Willie: I need that stone to defeat Thanos.",
        "Sorcerer Supreme: You wield a shield, not magic. Why do you need it?",
        "Captain Willie: With your help, I can send Thanos packing."
    ],
    "Stormbreak": [
        "Stormbreak: I require the stone for my gauntlet.",
        "Sorcerer Supreme: Magic is not your expertise, warrior.",
        "Stormbreak: But with it, I can become unstoppable!"
    ]
}

# Questions from Sorcerer Supreme and options
questions = [
    {"text": "Sorcerer Supreme: Why should I help you?", "options": ["For the greater good", "I can reward you"]},
    {"text": "Sorcerer Supreme: What will you do with the stone?", "options": ["Defeat Thanos", "Keep it for myself"]}
]

# Function to handle dialogue
def draw_dialogue(selected_hero):
    global dialogue_index
    if dialogue_index < len(dialogues[selected_hero]):
        text_surface = font.render(dialogues[selected_hero][dialogue_index], True, White)
        Window.blit(text_surface, (50, 50))
    else:
        current_state = question_state  # Move to question state after dialogues

# Function to handle questions
def draw_question():
    global question_index
    question_text = font.render(questions[question_index]["text"], True, White)
    Window.blit(question_text, (50, 50))
    
    # Draw options as buttons
    option_1_button = Button(50, 100, text=questions[question_index]["options"][0])
    option_2_button = Button(50, 150, text=questions[question_index]["options"][1])
    option_1_button.draw(Window)
    option_2_button.draw(Window)
    
    return option_1_button, option_2_button

# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If quit button clicked
            running = False  # Exit the loop and quits the game
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == character_selection:
                if character_1.is_clicked(event.pos):
                    selected_hero_img = "Iron Warrior"  # set selected hero to Iron Warrior
                    current_state = negotiation_state  # change state to negotiation

                elif character_2.is_clicked(event.pos): 
                    selected_hero_img = "Captain Willie"
                    current_state = negotiation_state
                
                elif character_3.is_clicked(event.pos):
                    selected_hero_img = "Stormbreak"
                    current_state = negotiation_state
        
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if current_state == negotiation_state:
                dialogue_index += 1  # Move to the next dialogue line
                if dialogue_index >= len(dialogues[selected_hero_img]):
                    current_state = question_state  # Move to question state
            elif current_state == question_state:
                question_index += 1  # Move to the next question after the answer is selected
                if question_index >= len(questions):
                    print("End of negotiation.")
                    pygame.quit()
                    sys.exit()

    Window.blit(image, (0, 0))  # Draw background image

    if current_state == character_selection:
        character_1.draw(Window)  # Draw Iron Warrior
        character_2.draw(Window)
        character_3.draw(Window)
        
    elif current_state == negotiation_state:
        if selected_hero_img:
            if selected_hero_img == "Iron Warrior":
                Window.blit(character_1_img, (100, 130))  # Draw Iron Warrior
            elif selected_hero_img == "Captain Willie":
                Window.blit(character_2_img, (100, 130))  # Draw Captain Willie
            elif selected_hero_img == "Stormbreak":
                Window.blit(character_3_img, (100, 130))  # Draw Stormbreak
            
            Window.blit(character_4_img, (300,130))  # Draw Sorcerer Supreme
            draw_dialogue(selected_hero_img)  # Display negotiation dialogue
    
    elif current_state == question_state:
        option_1_button, option_2_button = draw_question()  # Display question with options

        if event.type == pygame.MOUSEBUTTONDOWN:
            if option_1_button.is_clicked(event.pos):
                print(f"Selected option: {questions[question_index]['options'][0]}")
                current_state = dialogue_state
            elif option_2_button.is_clicked(event.pos):
                print(f"Selected option: {questions[question_index]['options'][1]}")
                current_state = dialogue_state

    pygame.display.flip()  # Update the display

pygame.quit()
sys.exit()
