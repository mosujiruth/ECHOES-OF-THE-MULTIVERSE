import pygame
import sys
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
width, height = 600, 400
puzzle_size = 300  # Adjust puzzle size to fit within the new dimensions
piece_size = puzzle_size // 4  # Each piece is 1/4 of the puzzle size (4x4 grid)

# Create the screen
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
is_fullscreen = False  # Initialize fullscreen state
char_1 = pygame.image.load("iron warrior.png").convert_alpha()
char_2 = pygame.image.load("captainwillie.png").convert_alpha()
char_3 = pygame.image.load("stormbreak.png").convert_alpha()

# Window picture
background = pygame.image.load('asgard.jpg').convert()
background = pygame.transform.scale(background, (width, height))

snap_sound = pygame.mixer.Sound('click.wav') 

def toggle_fullscreen():
    global screen, is_fullscreen, width, height, background
    if is_fullscreen:
        width, height = 600, 400  
        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE | pygame.SCALED)  
        is_fullscreen = False
    else:
        info = pygame.display.Info()
        width, height = info.current_w, info.current_h  
        screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)  
        is_fullscreen = True

    # Resize the background for the new screen dimensions
    background = pygame.image.load('asgard.jpg').convert()
    background = pygame.transform.scale(background, (width, height))


welcome_screen = "Welcome_to_asgard"
treasure_room = "treasure_room"
puzzle_room = "puzzle_complete"
next_level = "next_level"


puzzle_image = pygame.image.load('tesseract.jpg')
puzzle_image = pygame.transform.scale(puzzle_image, (puzzle_size, puzzle_size))

def snap_sound_blit():
    snap_sound.play()


# Break the picture into 16 pieces (4x4)
pieces = [
    puzzle_image.subsurface((x * piece_size, y * piece_size, piece_size, piece_size))
    for y in range(4) for x in range(4)
]

# Grid positions (A to P for 16 grids)
grid_positions = [
    (width // 2 - puzzle_size // 2 + (i % 4) * piece_size, height // 2 - puzzle_size // 2 + (i // 4) * piece_size)
    for i in range(16)
]
grid_labels = [chr(65 + i) for i in range(16)]  # Alphabet labels A to P

# Randomize puzzle piece positions
def randomize_positions():
    return [
        (random.randint(0, width - piece_size), random.randint(0, height - piece_size))
        for _ in range(16)
    ]

# Initial random positions
positions = randomize_positions()

# Game state variables
selected_piece = None
offset_x = 0
offset_y = 0
solved = [False] * 16
font = pygame.font.Font(None, 36)
try_again = False
try_again_timer = 0

# Draw welcome screen
def draw_welcome_screen():
    small_font = pygame.font.Font(None, 24) 
    text = small_font.render("Welcome to Asgard! Press any key to enter the treasure room.", True, (0, 255, 255))
    screen.blit(text, (15, 200))

# Draw treasure room
def draw_treasure_room():
    text = font.render("Solve the puzzle to get the Space Stone.", True, (0, 255, 255))
    screen.blit(text, (90, 30))

    # Draw grid with labels
    for i, pos in enumerate(grid_positions):
        pygame.draw.rect(screen, (255, 255, 255), (*pos, piece_size, piece_size), 3)
        label = font.render(grid_labels[i], True, (255, 255, 255))
        screen.blit(label, (pos[0] + 10, pos[1] + 10))
    
    # Draw puzzle pieces with numbers
    for i, (pos, piece) in enumerate(zip(positions, pieces)):
        screen.blit(piece, pos)  # Draw the piece
       

# Draw try again message
def draw_try_again():
    text = font.render("Try Again!", True, (255, 0, 0))
    screen.blit(text, (300, 250))

# Draw puzzle complete screen
def draw_puzzle_complete():
    text = font.render("Congrats warrior! Press any key to proceed.", True, (0, 255, 0))
    text_rect = text.get_rect(center=(width // 2, height // 2))  # Center on the screen
    screen.blit(text, text_rect)

# Main function
def start_level_5(selected_chara):
    global selected_piece, offset_x, offset_y, positions, try_again, try_again_timer
    current_state = welcome_screen
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.blit(background, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if current_state == welcome_screen:
                    current_state = treasure_room
                elif current_state == puzzle_room:
                    current_state = next_level
                
                # Toggle fullscreen
                if event.key == pygame.K_f:  
                    toggle_fullscreen()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_state == treasure_room:
                    for i, pos in enumerate(positions):
                        rect = pygame.Rect(pos[0], pos[1], piece_size, piece_size)
                        if rect.collidepoint(event.pos):
                            selected_piece = i
                            offset_x = pos[0] - event.pos[0]
                            offset_y = pos[1] - event.pos[1]
                            break

            if event.type == pygame.MOUSEBUTTONUP:
                if current_state == treasure_room and selected_piece is not None:
                    snapped = False
                    
                    # Check if the piece is dropped near a grid position
                    for i, grid_pos in enumerate(grid_positions):
                        if abs(positions[selected_piece][0] - grid_pos[0]) < 50 and \
                           abs(positions[selected_piece][1] - grid_pos[1]) < 50:
                            # Snap the piece to the grid if it is the correct position
                            if selected_piece == i:
                                snap_sound.play()
                                positions[selected_piece] = grid_pos
                                solved[selected_piece] = True
                            snapped = True
                            break
                    
                    if snapped and selected_piece != i:  # Only trigger "Try Again" if snapped but wrong grid
                        try_again = True
                        try_again_timer = pygame.time.get_ticks()

                    selected_piece = None  # Deselect piece after mouse up

            if event.type == pygame.MOUSEMOTION:
                if current_state == treasure_room and selected_piece is not None:
                    positions[selected_piece] = (event.pos[0] + offset_x, event.pos[1] + offset_y)

        
        if current_state == welcome_screen:
            draw_welcome_screen()
        elif current_state == treasure_room:
            draw_treasure_room()
            if all(solved):
                current_state = puzzle_room
        elif current_state == puzzle_room:
            draw_puzzle_complete()
            
        elif current_state == next_level:
            import level_6
            level_6.start_level_6(selected_chara)

        
        if try_again:
            draw_try_again()
            if pygame.time.get_ticks() - try_again_timer > 2000:
                try_again = False
                
                positions = randomize_positions() 

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
