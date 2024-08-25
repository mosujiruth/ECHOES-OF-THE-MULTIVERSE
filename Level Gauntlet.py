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
image=pygame.transform.scale(image,(screen_width,screen_height))

# Hero details
heroes = {
    "Iron Warrior": {"image": pygame.image.load("images/iron warrior.png"), "dialogue": ["I am Iron Warrior.", "Let's save the world!"]},
    "Captain Willie": {"image": pygame.image.load("images/captainwille.png"), "dialogue": ["Captain Willie here.", "Ready for battle!"]},
    "Stormbreak": {"image": pygame.image.load("images/stormbreak.png"), "dialogue": ["Stormbreak in the house!", "Let's rock!"]}
}

# Resize hero images
for hero in heroes:
    heroes[hero]["image"] = pygame.transform.scale(heroes[hero]["image"], (150, 150))

# Assume these are the selected heroes (could be based on user input)
selected_heroes = ["Iron Warrior", "Captain Willie", "Stormbreak"]  # This can be dynamic based on the actual selection

# Display dialogues based on hero selection
def show_dialogues():
    for hero_name in selected_heroes:
        if hero_name == "Iron Warrior":
            dialogues = heroes[hero_name]["dialogue"]
        elif hero_name == "Captain Willie":
            dialogues = heroes[hero_name]["dialogue"]
        elif hero_name == "Stormbreak":
            dialogues = heroes[hero_name]["dialogue"]
        else:
            dialogues = ["Unknown hero..."]

        for dialogue in dialogues:
            # Main loop
            run = True
            while run:
                 #Handles events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit() 
                if event.type == pygame.KEYDOWN:  # Skip to the next dialogue on key press
                    run = False

            #Image appeared
            Window.blit(image, (0,0))

            # Display hero images and dialogue
            for i, hero in enumerate(selected_heroes):
                Window.blit(heroes[hero]["image"], (50 + i * 200, 150))  # Adjust position as needed


            dialogue_text = font.render(dialogue, True, Black)
            Window.blit(dialogue_text, (50, 50))

# Main loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Display background image
    Window.blit(image, (0, 0))

    # Display hero images based on selection
    if len(selected_heroes) == 3:
        for i, hero in enumerate(selected_heroes):
            Window.blit(heroes[hero]["image"], (50 + i * 200, 300))  # Adjust position as needed
    elif len(selected_heroes) == 2:
        for i, hero in enumerate(selected_heroes):
            Window.blit(heroes[hero]["image"], (150 + i * 250, 300))  # Centered for 2 heroes
    elif len(selected_heroes) == 1:
        Window.blit(heroes[selected_heroes[0]]["image"], (325, 300))  # Centered for 1 hero
    else:
        print("No heroes selected!")
   
        #Updating Window
        pygame.display.flip()

        # Start the dialogue sequence
    if run:  # Only run dialogues if the window hasn't been closed
        show_dialogues()

    run = False  # End loop after showing dialogues

    
#Quit pygame and exit program               
pygame.quit()
sys.exit()
    