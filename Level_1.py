import pygame
import sys
from moviepy.editor import VideoFileClip  

# Initialize pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()


screen_width = 600
screen_height = 400


White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)


Window = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Level 1: Obtaining Gauntlet")


font = pygame.font.SysFont('Comic Sans MS', 11)
is_fullscreen = False

image = pygame.image.load("Warrior_Lab.png")
image = pygame.transform.scale(image, (screen_width, screen_height))


character_1_img = pygame.image.load("iron warrior.png").convert_alpha()
character_2_img = pygame.image.load("captainwillie.png").convert_alpha()
character_3_img = pygame.image.load("stormbreak.png").convert_alpha()


character_1_img = pygame.transform.scale(character_1_img, (180, 170))
character_2_img = pygame.transform.scale(character_2_img, (190, 170))
character_3_img = pygame.transform.scale(character_3_img, (110, 170))


Captain_Willie_Shield = pygame.image.load("Captain_Willie_Shield.png").convert_alpha()
Captain_Willie_Shield = pygame.transform.scale(Captain_Willie_Shield, (100, 100))

# Try loading the EagleEye bow image, handle errors if it fails
try:
    EagleEye_bow = pygame.image.load("EagleEye_bow.png").convert_alpha()
    EagleEye_bow = pygame.transform.scale(EagleEye_bow, (100, 100))
except pygame.error as e:
    print(f"Error loading EagleEye_bow image: {e}")
    EagleEye_bow = None  # Prevent crashes by setting to None if loading fails

# Load video clip using MoviePy
video_clip = VideoFileClip("IronWarrior_Gauntlet.mp4")  # Ensure you have the correct file extension

# Load button click sound
button_click_sound = pygame.mixer.Sound("Bitter.wav")

# Function to play button click sound
def play_button_click_sound():
    button_click_sound.play()

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

class Character:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)


character_1 = Character(character_1_img, 75, 110)
character_2 = Character(character_2_img, 230, 110)
character_3 = Character(character_3_img, 380, 110)

# Game states
level_1_dialogue = 1  # Game state for dialogue
level_1_options = 2  # Game state for options
dialogue_state = 3  # Game state for displaying dialogue after correct option
current_state = level_1_dialogue  
selected_hero = None  # Variable stores selected hero


dialogue_index = 0
dialogue_displayed = False

options = []  # This will hold Button objects for each option
correct_option_index = 0  # Placeholder for the correct option
options_displayed = False  # Track if options have been displayed

def toggle_fullscreen():
    global is_fullscreen, Window
    if is_fullscreen:
       Window = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    else:
       Window = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE | pygame.SCALED)

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

# Function to play video using Pygame
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

def restart_level():
    global current_state, dialogue_index
    current_state = level_1_dialogue
    dialogue_index = 0
    options.clear()

def start_level_1(selected_chara):
    global selected_hero, current_state, dialogue_index
    if selected_chara == "IRON WARRIOR":
        selected_hero = character_1
    elif selected_chara == "CAPTAIN WILLIE":
        selected_hero = character_2
    elif selected_chara == "STORMBREAK":
        selected_hero = character_3
    else:
        print("Invalid character selected!")
        return

    running = True
    play_video = False
    

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if current_state == level_1_dialogue:
                        if selected_hero == character_1:
                            create_options(["Use Captain Willie's Shield", "Use EagleEye's Bow"], 0)
                        elif selected_hero == character_2:
                            create_options(["Iron Warrior", "Wizard Supreme"], 0)
                        elif selected_hero == character_3:
                            create_options(["Iron Warrior", "Blue Skull"], 0)
                        current_state = level_1_options
                    elif current_state == dialogue_state:
                        dialogue_index += 1
                        if selected_hero == character_2 and dialogue_index == 6:
                            play_video = True
                            running = False
                        elif selected_hero == character_3 and dialogue_index == 6:
                            play_video = True
                            running = False
                        elif selected_hero == character_1 and dialogue_index == 1:
                            play_video = True
                            running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_state == level_1_options:
                    for i, option in enumerate(options):
                        if option.is_clicked(event.pos):
                            button_click_sound.play()
                            if i == correct_option_index:
                                dialogue_index = 0
                                current_state = dialogue_state
                            else:
                                restart_level()

        Window.blit(image, (0, 0))

        if current_state == level_1_dialogue:
            if selected_hero == character_1:
                character_1.draw(Window)
                draw_bubble("Which item should we use to make a gauntlet?", (character_1.rect.x, character_1.rect.y - 40))
                Window.blit(Captain_Willie_Shield, (character_1.rect.x + 320, character_1.rect.y + 50))
                if EagleEye_bow:
                    Window.blit(EagleEye_bow, (character_1.rect.x + 200, character_1.rect.y + 50))
            elif selected_hero == character_2:
                character_2.draw(Window)
                draw_bubble("Who should we ask for help?", (character_2.rect.x, character_2.rect.y - 40))
            elif selected_hero == character_3:
                character_3.draw(Window)
                draw_bubble("Who is able to make me a gauntlet?", (character_3.rect.x, character_3.rect.y - 40))

        elif current_state == level_1_options:
            for option in options:
                option.draw(Window)

        elif current_state == dialogue_state:
            if selected_hero == character_1:
                if dialogue_index < 1:
                    draw_bubble("Let's begin melting this shield.", (character_1.rect.x, character_1.rect.y - 40))
                    Window.blit(Captain_Willie_Shield, (character_1.rect.x + 200, character_1.rect.y + 50))
                    character_1.draw(Window)
            elif selected_hero == character_2:
                character_2.draw(Window)
                character_1.draw(Window)
                if dialogue_index < 6:
                    if dialogue_index % 2 == 0:
                        draw_bubble(["Hey Iron Warrior, can you do me a help?",
                                     "I need a gauntlet to defeat Titan.",
                                     "Thanks Iron Warrior"][dialogue_index // 2],
                                    (character_2.rect.x, character_2.rect.y - 40))
                    else:
                        draw_bubble(["What can I help you with, Cap?",
                                     "Okay Cap, I'll do the gauntlet ASAP",
                                     "Don't mention it, Cap"][dialogue_index // 2],
                                    (character_1.rect.x, character_1.rect.y - 40))
            elif selected_hero == character_3:
                character_3.draw(Window)
                character_1.draw(Window)
                if dialogue_index < 6:
                    if dialogue_index % 2 == 0:
                        draw_bubble(["Hey Iron Warrior, I need your help.",
                                     "I need a gauntlet to destroy Titan.",
                                     "Alright then Iron Warrior, see you soon"][dialogue_index // 2],
                                    (character_3.rect.x, character_3.rect.y - 40))
                    else:
                        draw_bubble(["Yo Stormbreak, what can I help you with?",
                                     "Sure thing, will get it done soon",
                                     "Okay Stormbreak, see ya"][dialogue_index // 2],
                                    (character_1.rect.x, character_1.rect.y - 40))

        pygame.display.update()

        if play_video:
            if not play_video_in_pygame(video_clip):
                running = False
                import Level_2
                Level_2.start_level_2(selected_chara)
    pygame.quit()
    sys.exit()
