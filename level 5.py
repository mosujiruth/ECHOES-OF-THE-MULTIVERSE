import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
puzzle_size = 400  
piece_size = puzzle_size // 2  

# Create the screen
screen = pygame.display.set_mode((width, height))

# Set background image
background = pygame.image.load('asgard.jpg').convert()
background = pygame.transform.scale(background, (width, height))

# Game stages
welcome_screen = "Welcome_to_asgard"
treasure_room = "treasure_room"
puzzle_room = "puzzle_complete"
next_level = "next_level"

# Puzzle image
puzzle_image = pygame.image.load('tesseract.avif')
puzzle_image = pygame.transform.scale(puzzle_image, (puzzle_size, puzzle_size))

# Split the image into 4 pieces (2x2 grid)
pieces = [
    puzzle_image.subsurface((0, 0, piece_size, piece_size)),
    puzzle_image.subsurface((piece_size, 0, piece_size, piece_size)),
    puzzle_image.subsurface((0, piece_size, piece_size, piece_size)),
    puzzle_image.subsurface((piece_size, piece_size, piece_size, piece_size))
]

# Randomize positions of puzzle pieces
positions = [
    (random.randint(0, width - piece_size), random.randint(0, height - piece_size))
    for _ in range(4)
]

# Track selected piece
selected_piece = None
offset_x = 0
offset_y = 0

# Puzzle grid and solved state tracking
correct_positions = [(200, 100), (400, 100), (200, 300), (400, 300)]
solved = [False, False, False, False]

def draw_welcome_screen():
    font = pygame.font.Font(None, 36)
    text = font.render("Welcome to Asgard! Press any key to enter the treasure room.", True, (255, 255, 255))
    screen.blit(text, (100, 250))

def draw_treasure_room():
    font = pygame.font.Font(None, 36)
    text = font.render("Solve the puzzle to get the Space Stone.", True, (255, 255, 255))
    screen.blit(text, (150, 50))
    
    # Draw puzzle pieces
    for i, (pos, piece) in enumerate(zip(positions, pieces)):
        if not solved[i]:
            screen.blit(piece, pos)

def draw_puzzle_complete():
    font = pygame.font.Font(None, 36)
    text = font.render("Congrats warrior! Press any key to proceed.", True, (255, 255, 255))
    screen.blit(text, (200, 250))

def main():
    global selected_piece, offset_x, offset_y
    current_state = welcome_screen
    running = True
    clock = pygame.time.Clock()  # Create a clock to cap the frame rate

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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_state == treasure_room:
                    for i, pos in enumerate(positions):
                        if not solved[i]:
                            rect = pygame.Rect(pos[0], pos[1], piece_size, piece_size)
                            if rect.collidepoint(event.pos):
                                selected_piece = i
                                offset_x = pos[0] - event.pos[0]
                                offset_y = pos[1] - event.pos[1]
                                break

            if event.type == pygame.MOUSEBUTTONUP:
                if current_state == treasure_room and selected_piece is not None:
                    # Check if the piece is placed correctly
                    if abs(positions[selected_piece][0] - correct_positions[selected_piece][0]) < 50 and \
                       abs(positions[selected_piece][1] - correct_positions[selected_piece][1]) < 50:
                        positions[selected_piece] = correct_positions[selected_piece]
                        solved[selected_piece] = True
                    selected_piece = None

            if event.type == pygame.MOUSEMOTION:
                if current_state == treasure_room and selected_piece is not None:
                    positions[selected_piece] = (event.pos[0] + offset_x, event.pos[1] + offset_y)

        # Drawing based on the current state
        if current_state == welcome_screen:
            draw_welcome_screen()
        elif current_state == treasure_room:
            draw_treasure_room()
            if all(solved):
                current_state = puzzle_room
        elif current_state == puzzle_room:
            draw_puzzle_complete()
        elif current_state == next_level:
            pygame.display.set_caption("Level 6")
            pygame.display.flip()  # Ensure the display is updated before the delay
            pygame.time.delay(3000)  # Pause for 3 seconds before exiting
            pygame.quit()
            sys.exit()

        pygame.display.flip()  # Update the screen
        clock.tick(60)  # Cap the frame rate at 60 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

