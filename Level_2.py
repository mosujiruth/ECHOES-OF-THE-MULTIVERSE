import pygame
import sys
from moviepy.editor import VideoFileClip  


pygame.init()
pygame.font.init()
pygame.mixer.init()


screen_width = 600
screen_height = 400


White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)


Window = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Level 2: Convince Wizard Supreme")


font = pygame.font.SysFont('Comic Sans MS', 13)


image = pygame.image.load("Strange_Office.png")
image = pygame.transform.scale(image, (screen_width, screen_height))


character_1_img = pygame.image.load("iron warrior.png").convert_alpha()
character_2_img = pygame.image.load('captainwillie.png').convert_alpha()
character_3_img = pygame.image.load("stormbreak.png").convert_alpha()


character_1_img = pygame.transform.scale(character_1_img, (170, 200))
character_2_img = pygame.transform.scale(character_2_img, (180, 200))
character_3_img = pygame.transform.scale(character_3_img, (110, 200))


character_4_img = pygame.image.load("Wizard_Supreme.jpg").convert_alpha()
character_4_img = pygame.transform.scale(character_4_img, (230, 200))

# Load button click sound
button_click_sound = pygame.mixer.Sound("Bitter.wav")

# Function to play button click sound
def play_button_click_sound():
    button_click_sound.play()

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

class Character:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
# Use this to click on heroes
character_1 = Character(character_1_img, 70, 130)
character_2 = Character(character_2_img, 250, 130)
character_3 = Character(character_3_img, 450, 130)



instruction_screen=1
negotiation_state = 2  # Game state for negotiation
question_state = 3  # Game state for question
end_state = 4  # Game end state
current_state = negotiation_state  # Set the current state to character selection
selected_hero = None  # Variable stores selected hero

# Dialogue index for negotiation
dialogue_index = 0
question_index = 0

# Flags to control question display
show_question_1 = False
show_question_2 = False
show_question_3 = False

# Updated dialogues
dialogues = {
    "Iron Warrior": [
        "Iron Warrior: Good day to you, Wizard",
        "Wizard Supreme: Why are you here?",
        "Iron Warrior: Well I'm here for the Reality Stone",
        "Wizard Supreme: Okay I will give it to you",
        "Iron Warrior: Thanks Wizard",
        "Wizard Supreme: Umm no, hold your thanks until I gain trust on you",
        "Iron Warrior: Well, I expected that",
        "Wizard Supreme: Do you promise you would use the stone to destroy Titan and not us?",
        "Iron Warrior: Of course not, I don't betray my people",
        "Wizard Supreme: Well there is one last question since you are a human",
        "Iron Warrior: Well, go on",
        "Wizard Supreme: Do you think you can handle this much of power?",
        "Iron Warrior: Ofcourse Wizard, I'm built different"
    ],
    "Captain Willie": [
        "Captain Willie: Good day to you, Wizard",
        "Wizard Supreme: Why did you come finding me?",
        "Captain Willie: Well, I came to ask you for the Reality Stone",
        "Wizard Supreme: But I will only give the Reality Stone to someone who will gain my trust.",
        "Captain Willie: Alright, tell how can I gain your trust Wizard?",
        "Wizard Supreme: Can you bare any consequences??",
        "Captain Willie: Yes Wizard, I'm positive I can handle it",
        "Wizard Supreme: Alright, this would be a final question",
        "Captain Willie: Yes finally we are almost done",
        "Wizard Supreme: What will you do with the stone after you won the battle?",
        "Captain Willie: Protect it"
    ],
    "Stormbreak": [
        "Stormbreak: Good day to you, Wizard",
        "Wizard Supreme: Why did you come all the way from Asgard?",
        "Stormbreak: Well, I came to ask you for the Reality Stone.",
        "Wizard Supreme: Are you sure, you won't use is it for your own use?",
        "Stormbreak: Ofcourse not, Wizard",
        "Wizard Supreme: Fine, you can have the stone after you gain my trust",
        "Stormbreak: Alright, tell me how do I gain it?",
        "Wizard Supreme: Can you handle such mighty power?",
        "Stormbreak: As a God, I surely can handle anything.",
        "Wizard Supreme: Okay here is the final question",
        "Stormbreak: Yes, finally",
        "Wizard Supreme: What would you do with the Stone once the war ended?",
        "Stormbreak: Protect it, so it doesn't fall in wrong hands"
    ]
}

# Questions are based on the Dialogue(Story)
questions = {
    "Iron Warrior": [
        {"text": "Why did Iron Warrior came to visit Wizard Supreme?", "options": ["To take the Reality Stone", "To take the Time Stone"], "correct_option": 0},
        {"text": "What does the Iron Warrior promise to do with the Reality Stone?", "options": ["To Betray his people", "To Destroy Titan"], "correct_option": 1},
        {"text": "Why did Wizard Supreme asked Iron Warrior if he ould handle this much of power?", "options": ["Because he is a Human", "Because he is a God"], "correct_option": 0}
    ],
    "Captain Willie": [
        {"text": "Why did Captain Willie came finding Wizard Supreme?", "options": ["To take the Space Stone", "To take the Reality Stone"], "correct_option": 1},
        {"text": "What did Wizard Supreme asked Captain Willie?", "options": ["If he can bare any consequences", "If he could save the world"], "correct_option": 0},
        {"text": "What was Captain Willie's answer to the last question?", "options": ["Protect the Stone", "Destroy the Stone"], "correct_option": 0},
    ],
    "Stormbreak": [
        {"text": "Why did Stormbreak came from Asgard?", "options": ["For the Mind Stone", "For the Reality Stone"], "correct_option": 1},
        {"text": "What did Wizard Supreme asked Stormbreak?", "options": ["If he could handle such Mighty Power", "If he could destroy Titan"], "correct_option": 0},
        {"text": "What was Stormbreak's answer to the last question?", "options": ["Protect it", "Destroy it"], "correct_option": 0}
    ]
}
is_fullscreen=False
def toggle_fullscreen():
    global is_fullscreen, Window
    if is_fullscreen:
       Window = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    else:
       Window = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE | pygame.SCALED)



def draw_instruction_screen():
    
    instruction_bgg = pygame.image.load("strange-room.png")
    instruction_bgg=pygame.transform.scale(instruction_bgg,(screen_width,screen_height))
    small_font = pygame.font.Font(None, 24)  # Change font size to a smaller value
    Window.blit(instruction_bgg, (0, 0))
    instruction_text = small_font.render("Finish the quiz to obtain the time stone", True, White)
    continue_text1 = small_font.render("Read the dialogues properly to answer the quiz ", True, White)
    continue_text2 = small_font.render("Press SPACE to continue", True, White)
    Window.blit(instruction_text, (screen_width//2 - instruction_text.get_width()//2, screen_height//4))
    Window.blit(continue_text1, (screen_width//2 - continue_text1.get_width()//2, screen_height//3.5))
    Window.blit(continue_text2, (screen_width//2 - continue_text2.get_width()//2, screen_height//2.5))
    pygame.display.flip()

try_again_message = ""
# Function to play video using MoviePy and Pygame
def play_video_in_pygame(video_clip, delay=100):
    for frame in video_clip.iter_frames(fps=30, dtype='uint8'):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return False

        # Convert the frame to Pygame Surface
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        frame_surface = pygame.transform.scale(frame_surface, (screen_width, screen_height))

        # Draw frame on screen
        Window.blit(frame_surface, (0, 0))
        pygame.display.update()

        # Delay for each frame to slow down the video (delay in milliseconds)
        pygame.time.delay(delay)

    return True

# Load AI-generated video (replace with the actual file path)
ai_video_clip = VideoFileClip("WizardHouse_Entry.mp4")

def draw_dialogue(selected_hero):
    global dialogue_index, current_state
    
    # Show dialogue as long as there's dialogue left
    if dialogue_index < len(dialogues[selected_hero]):
        text_surface = font.render(dialogues[selected_hero][dialogue_index], True, White)
        Window.blit(text_surface, (50, 50))
    else:
        # All dialogues have been displayed, move to question state
        current_state = question_state
        dialogue_index = 0  # Reset dialogue index for future use

def draw_question(selected_hero):
    global question_index, try_again_message
    if question_index < len(questions[selected_hero]): 
        question_text = font.render(questions[selected_hero][question_index]["text"], True, White)
        Window.blit(question_text, (50, 50))
        
        option_1_button = Button(50, 100, text=questions[selected_hero][question_index]["options"][0])
        option_2_button = Button(50, 150, text=questions[selected_hero][question_index]["options"][1])
        option_1_button.draw(Window)
        option_2_button.draw(Window)

        # Draw the try again message if it exists
        if try_again_message:
            message_surface = font.render(try_again_message, True, Red)
            Window.blit(message_surface, (50, 250))
    
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

def restart_level():
    global current_state, dialogue_index, question_index, selected_hero
    current_state = negotiation_state
    dialogue_index = 0
    question_index = 0
    selected_hero = None

def start_level_2(selected_chara):
    global selected_hero, current_state, dialogue_index, next_step, show_question_1, show_question_2, show_question_3, question_index,try_again_message
    
    # Initialize flags
    show_question_1 = False
    show_question_2 = False
    show_question_3 = False
    next_step = None
    
    # Set selected hero
    if selected_chara == "IRON WARRIOR":
        selected_hero = "Iron Warrior"
    elif selected_chara == "CAPTAIN WILLIE":
        selected_hero = "Captain Willie"
    elif selected_chara == "STORMBREAK":
        selected_hero = "Stormbreak"
    else:
        print("Invalid character selected!")
        restart_level()  
        return
    
    # Main Loop
    running = True
    play_video = True
    show_dialogue = True
    option_1_button = None
    option_2_button = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if current_state == instruction_screen:
                   current_state = negotiation_state
                elif event.key == pygame.K_r:  
                    restart_level()
            elif event.type == pygame.MOUSEBUTTONDOWN and current_state == question_state:
                option_1_button, option_2_button = draw_question(selected_hero)
                try_again_message = ""

                if option_1_button and option_1_button.is_clicked(event.pos):
                    button_click_sound.play()
                    if questions[selected_hero][question_index]["correct_option"] == 0:
                        question_index += 1
                        if question_index >= len(questions[selected_hero]):
                            current_state = end_state
                    else:
                        try_again_message = "Try again!"
                elif option_2_button and option_2_button.is_clicked(event.pos):
                    button_click_sound.play()
                    if questions[selected_hero][question_index]["correct_option"] == 1:
                        question_index += 1
                        if question_index >= len(questions[selected_hero]):
                            current_state = end_state
                    else:
                        try_again_message = "Try again!"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if current_state == negotiation_state:
                    if show_dialogue:
                        dialogue_index += 1
                        if dialogue_index >= len(dialogues[selected_hero]):
                            current_state = question_state
                        else:
                            show_dialogue = True

        # Redraw screen
        Window.blit(image, (0, 0))
        
        if play_video:
            play_video = play_video_in_pygame(ai_video_clip) # If the play_video flag is set to True, play the video using the play_video_in_pygame function.
            current_state = instruction_screen # This indicates that the game will now transition to the negotiation phase.
        
        elif current_state == instruction_screen:
            draw_instruction_screen()
        elif current_state == negotiation_state:  
            draw_selected_hero_and_wizard(selected_hero) 
            draw_dialogue(selected_hero) 
        
        elif current_state == question_state:
            draw_selected_hero_and_wizard(selected_hero) 
            draw_question(selected_hero) 
        
        elif current_state == end_state: 
            end_message = font.render('YOU RECEIVED THE REALITY STONE!', True, White) 
            Window.blit(end_message, (screen_width // 2 - end_message.get_width() // 2, screen_height // 2 - end_message.get_height() // 2)) 
            import Level_3 
            Level_3.start_level_3(selected_chara) 
        pygame.display.flip()

    pygame.quit()
    sys.exit()
