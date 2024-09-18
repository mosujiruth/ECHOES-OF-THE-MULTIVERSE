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
pygame.display.set_caption("Level 2: Convince Wizard Supreme")

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
character_4_img = pygame.transform.scale(character_4_img, (230, 200))

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
end_state = 4  # Game end state
current_state = character_selection  # Set the current state to character selection
selected_hero_img = None  # Variable stores selected hero

# Dialogue index for negotiation
dialogue_index = 0
question_index = 0

# Flags to control question display
show_question_1 = False
show_question_2 = False
show_question_3 = False

# Updated negotiation dialogues
dialogues = {
    "Iron Warrior": [
        "Iron Warrior: Good day to you, Wizard",
        "Wizard Supreme: Why are you here?",
        "Iron Warrior: Well I'm here for the Reality Stone",
        "Wizard Supreme: Okay I will give it to you",
        "Iron Warrior: Thanks Wizard",
        "Wizard Supreme: Umm no, hold your thanks until I gain trust on you",
        "Iron Warrior: Well, I expected that",
        "Wizard Supreme: Are you sure, you won't use it against us?",
        "Iron Warrior: Of course not, I don't betray my people",
        "Wizard Supreme: Well there is one last question since you are a human",
        "Iron Warrior: Well, go on",
        "Wizard Supreme: Okay you gained my trust, Iron Warrior",
        "Wizard Supreme: Here is the Reality Stone",
        "Iron Warrior: Thanks Wizard"
    ],
    "Captain Willie": [
        "Captain Willie: Good day to you, Wizard",
        "Wizard Supreme: Why did you come finding me?",
        "Captain Willie: Well, I'm came to ask you for the Reality Stone",
        "Wizard Supreme: But I will only give the Reality Stone to someone who will gain my trust.",
        "Captain Willie: Alright, tell how can I gain your trust Wizard?",
        "Wizard Supreme: Are you sure you bare the consequences?",
        "Captain Willie: Yes Wizard, I'm positive I can handle it",
        "Wizard Supreme: Alright, this would be a final question",
        "Captain Willie: Yes finally we are almost done",
        "Wizard Supreme: You have gained my trust, Cap",
        "Wizard Supreme: Here is the Reality Stone",
        "Captain Willie: Thank you, Wizard"
    ],
    "Stormbreak": [
        "Stormbreak: Good day to you, Wizard",
        "Wizard Supreme: Why did you come all the way from Asgard?",
        "Stormbreak: Well, I came you ask you for the Reality Stone.",
        "Wizard Supreme: Are you sure, you won't use is it for your own use?",
        "Stormbreak: Ofcourse not, Wizard",
        "Wizard Supreme: Fine, you can have the stone after you gain my trust",
        "Stormbreak: Alright, tell me how do I gain it?",
        "Wizard Supreme: Are you sure you can bare the consequences?",
        "Stormbreak: As a hero, I surely can handle anything.",
        "Wizard Supreme: Okay here is the final question",
        "Stormbreak: Yes, finally",
        "Wizard Supreme: Okay Stormbreak, here is the stone",
        "Stormbreak: Thank you, Wizard"
 
    ]
}

# Updated Marvel stone-related questions for each hero
questions = {
    "Iron Warrior": [
        {"text": "Why do you need the Reality Stone?", "options": ["To defeat Titan", "To be unstoppable"], "correct_option": 0},
        {"text": "What will you do with the Reality Stone if you succeed?", "options": ["Use it for personal gain", "Protect the universe"], "correct_option": 1},
        {"text": "Do you believe you're worthy of controlling such power?", "options": ["Yes", "No"], "correct_option": 0}
    ],
    "Captain Willie": [
        {"text": "Why do you need the Reality Stone?", "options": ["To Wipe-out half the population", "To destroy Titan"], "correct_option": 1},
        {"text": "How far will you go to protect the Reality Stone?", "options": ["As far as needed", "Not beyond limits"], "correct_option": 0},
        {"text": "What will you do with the Reality Stone once you defeated Titan?", "options": ["Protect the Reality Stone", "Destroy the Reality Stone"], "correct_option": 0},
    ],
    "Stormbreak": [
        {"text": "Why seek the Reality Stone?", "options": ["Gain Ultimate Power", "Protect this Universe "], "correct_option": 1},
        {"text": "Are you aware of the Reality Stone's sacrifice?", "options": ["Yes", "No"], "correct_option": 0},
        {"text": "Will you give up your possession for the Reality Stone?", "options": ["Yes", "No"], "correct_option": 0}
    ]
}

def draw_dialogue(selected_hero):
    global dialogue_index, show_question_1, show_question_2, show_question_3, current_state
    if dialogue_index < len(dialogues[selected_hero]):
        text_surface = font.render(dialogues[selected_hero][dialogue_index], True, White)
        Window.blit(text_surface, (50, 50))

        # Check specific dialogue lines to show questions
        if selected_hero == "Iron Warrior":
            if dialogues[selected_hero][dialogue_index] == "Iron Warrior: Well I'm here for the Reality Stone":
                show_question_1 = True
                current_state = question_state  # Move to question state after the dialogue``
                dialogue_index += 1  # Move to the next dialogue immediately

            elif dialogues[selected_hero][dialogue_index] == "Iron Warrior: Well, I expected that":
                show_question_2 = True
                current_state = question_state  # Move to question state after the dialogue
                dialogue_index += 1  # Move to the next dialogue immediately

            elif dialogues[selected_hero][dialogue_index] == "Iron Warrior: Well, go on":
                show_question_3 = True
                current_state = question_state  # Move to question state after the dialogue
                dialogue_index += 1  # Move to the next dialogue immediately


        elif selected_hero == "Captain Willie":
            if dialogues[selected_hero][dialogue_index] == "Captain Willie: Well, I'm came to ask you for the Reality Stone":
                show_question_1 = True
                current_state = question_state
                dialogue_index += 1

            elif dialogues[selected_hero][dialogue_index] == "Captain Willie: Alright, tell how can I gain your trust Wizard?":
                show_question_2 = True
                current_state = question_state
                dialogue_index += 1

            elif dialogues[selected_hero][dialogue_index] == "Captain Willie: Yes finally we are almost done":
                show_question_3 = True
                current_state = question_state
                dialogue_index += 1
        
        elif selected_hero == "Stormbreak":
            if dialogues[selected_hero][dialogue_index] == "Stormbreak: Well, I came you ask you for the Reality Stone.":
                show_question_1 = True
                current_state = question_state
                dialogue_index += 1

            elif dialogues[selected_hero][dialogue_index] == "Stormbreak: Alright, tell me how do I gain it?":
                show_question_2 = True
                current_state = question_state
                dialogue_index += 1

            elif dialogues[selected_hero][dialogue_index] == "Stormbreak: Yes, finally":
                show_question_3 = True
                current_state = question_state
                dialogue_index += 1

            


def draw_question(selected_hero):
    global question_index
    if question_index < len(questions[selected_hero]):
        question_text = font.render(questions[selected_hero][question_index]["text"], True, White)
        Window.blit(question_text, (50, 50))
    
        # Draw option buttons
        option_1_button = Button(50, 100, text=questions[selected_hero][question_index]["options"][0])
        option_2_button = Button(50, 150, text=questions[selected_hero][question_index]["options"][1])
        option_1_button.draw(Window)
        option_2_button.draw(Window)
    
        return option_1_button, option_2_button
    return None, None  # In case there are no questions left

def draw_selected_hero_and_wizard(selected_hero):
    if selected_hero == "Iron Warrior":
        Window.blit(character_1_img, (50, 200))
    elif selected_hero == "Captain Willie":
        Window.blit(character_2_img, (50, 200))
    elif selected_hero == "Stormbreak":
        Window.blit(character_3_img, (50, 200))
    
    Window.blit(character_4_img, (300, 200))

# Main Loop
running = True
show_dialogue = True
next_step = None
option_1_button = True
option_2_button = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == character_selection:
                if character_1.is_clicked(event.pos):
                    selected_hero_img = "Iron Warrior"
                    current_state = negotiation_state
                elif character_2.is_clicked(event.pos):
                    selected_hero_img = "Captain Willie"
                    current_state = negotiation_state
                elif character_3.is_clicked(event.pos):
                    selected_hero_img = "Stormbreak"
                    current_state = negotiation_state
        
            elif current_state == question_state:
                # Draw buttons and check if clicked
                option_1_button, option_2_button = draw_question(selected_hero_img)
                if option_1_button.is_clicked(event.pos):
                    if questions[selected_hero_img][question_index]["correct_option"] == 0:
                        question_index += 1
                        if question_index >= len(questions[selected_hero_img]):
                            current_state = end_state
                    else:
                        running = False
                elif option_2_button.is_clicked(event.pos):
                    if questions[selected_hero_img][question_index]["correct_option"] == 1:
                        question_index += 1
                        if question_index >= len(questions[selected_hero_img]):
                            current_state = end_state
                    else:
                        running = False


        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
          if current_state == negotiation_state:
            if show_dialogue:
                    dialogue_index += 1
                    if dialogue_index >= len(dialogues[selected_hero_img]):
                        show_dialogue = False
                    else:
                        if show_question_1 and dialogues[selected_hero_img][dialogue_index] == "Iron Warrior: Well I'm here for the Reality Stone":
                            show_dialogue = False
                            next_step = "first_question"
                            show_question_1 = False
                        
                        elif show_question_2 and dialogues[selected_hero_img][dialogue_index] == "Iron Warrior: Well, I expected that":
                            show_dialogue = False
                            next_step = "second_question"
                            show_question_2 = False
                        
                        elif show_question_3 and dialogues[selected_hero_img][dialogue_index] == "Iron Warrior: Well, go on":
                            show_dialogue = False
                            next_step = "third_question"
                            show_question_3 = False

    # Update Display
    Window.blit(image, (0, 0))  # Background image
    
    if current_state == character_selection:
        character_1.draw(Window)
        character_2.draw(Window)
        character_3.draw(Window)
    
    elif current_state == negotiation_state:
        draw_selected_hero_and_wizard(selected_hero_img)
        draw_dialogue(selected_hero_img)
    
    elif current_state == question_state:
        draw_selected_hero_and_wizard(selected_hero_img)
        draw_question(selected_hero_img)
    
    elif current_state == end_state:
        # Draw the end message
        end_message = font.render('YOU RECEIVED THE REALITY STONE!', True, White)
        Window.blit(end_message, (screen_width // 2 - end_message.get_width() // 2, screen_height // 2 - end_message.get_height() // 2))
    
    pygame.display.flip()

pygame.quit()
sys.exit()
