import pygame
import sys

#bringing in pygame
pygame.init()

#Bringing in font
pygame.font.init()

# Set Screen width and height
screen_width = 600
screen_height = 400

#Define colours
White = (255,255,255)
Black = (0,0,0)

# Create the window 
Window = pygame.display.set_mode((screen_width, screen_height))
# Caption being popped up in the display
pygame.display.set_caption("Level 1: Obtaining Gauntlet")
# Choosing font type
font = pygame.font.SysFont('Comic Sans MS ', 30)

# Displaying Stark Office Background
image=pygame.image.load("Stark_Lab.png")
# Scaling the image according to the screen width and screen height
image=pygame.transform.scale(image, (screen_width, screen_height))

# Hero details
character_1 = pygame.image.load("iron warrior.png").convert_alpha()
character_2 = pygame.image.load('captainwillie.png').convert_alpha()
character_3 = pygame.image.load("stormbreak.png").convert_alpha()

#Scaling hero 
character_1 = pygame.transform.scale(character_1, (180, 170))
character_2 = pygame.transform.scale(character_2, (190, 170))
character_3 = pygame.transform.scale(character_3, (110, 170))

# Assume these are the selected heroes (could be based on user input)
selected_heroes = ["Iron Warrior", "Captain Willie", "Stormbreak"]  # This can be dynamic based on the actual selection

# Dialogue list
dialogue = [
    "Iron Warrior: Yoo, what's good Cap/Stormbreak?",
    "Captain Willie: I'm good Iron Warrior, what about you?",
    "Stormbreak: Same here, how you doing iron warrior?",
    "Iron Warrior: Nice, It's great to meet you guys after a long time.",
    "Captain Willie: Yes, it's great we get to meet again. But we are here for your help Iron Warrior.",
    "Iron Warrior: Tell me what can I help you with?",
    "Stormbreak: Okay here it is, we need a exact Gauntlet like Thanos have so that when we find the all 6 stones we can send Thanos and his troops back from we they came before he do it to us.",
    "Iron Warrior: Okay sounds good to me but what do I get in return if I help you guys?",
    "Captain Willie: Well, there is nothing I can give you but if u don't help then Thanos might wipe half the population in the world.",
    "Stormbreak: Half of the population and our families could be in it Iron Warrior.",
    "Iron Warrior: Alright i'll do it for my daughter, sorry I forgot her name.",
]

# Dialouge index
dialogue_index = 0

# Main loop
run = True
while run:
    #Handles events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() 
        if event.type == pygame.KEYDOWN:  # Skip to the next dialogue on key press
            dialogue_index += 1
            if dialogue_index >= len(dialogue):
                dialogue_index = 0

    # Display background image
    Window.blit(image, (0, 0))

    #Display hero images on window
    Window.blit(character_1, (450, 200))
    Window.blit(character_2, (10, 200))
    Window.blit(character_3, (130, 200))

    # Display the current dialogue text
    if dialogue_index < len(dialogue):
        text_surface = font.render(dialogue[dialogue_index], True, White)
        text_rect = text_surface.get_rect(center=(screen_width // 2, 90))
        Window.blit(text_surface, text_rect)  # Adjust position as needed
   
    #Updating Window
    pygame.display.flip()
    
#Quit pygame and exit program               
pygame.quit()
sys.exit()