import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
puzzle_size = 400  # Adjust puzzle size if needed
piece_size = puzzle_size // 4  # Each piece is now 1/4 of the puzzle size (4x4 grid)

# Create the screen
screen = pygame.display.set_mode((width, height))

# window pic
background = pygame.image.load('asgard.jpg').convert()
background = pygame.transform.scale(background, (width, height))

# Game stages
welcome_screen = "Welcome_to_asgard"
treasure_room = "treasure_room"
puzzle_room = "puzzle_complete"
next_level = "next_level"
try_again_state = "try_again"

# display puzzle pic
puzzle_image = pygame.image.load('tesseract.avif')
puzzle_image = pygame.transform.scale(puzzle_image, (puzzle_size, puzzle_size))

# Break the pic into 16 pieces (4x4)
pieces = [
    puzzle_image.subsurface((x * piece_size, y * piece_size, piece_size, piece_size))
    for y in range(4) for x in range(4)
]

# Grid positions (A to P for 16 grids)
grid_positions = [
    (200 + (i % 4) * piece_size, 100 + (i // 4) * piece_size) for i in range(16)
]
grid_labels = [chr(65 + i) for i in range(16)]  # Alphabet labels A to P

# Randomize puzzle piece positions (Ensure they stay within bounds)
def randomize_positions():
    return [
        (random.randint(0, width - piece_size), random.randint(0, height - piece_size))
        for _ in range(16)
    ]

# Initial random positions
positions = randomize_positions()

# Puzzle numbers 1 to 16
piece_numbers = list(range(1, 17))

# Game state variables
selected_piece = None
offset_x = 0
offset_y = 0
solved = [False] * 16
font = pygame.font.Font(None, 36)
try_again = False
try_again_timer = 0

# Re-randomize button
button_rect = pygame.Rect(600, 500, 150, 50)

# Draw welcome screen
def draw_welcome_screen():
    text = font.render("Welcome to Asgard! Press any key to enter the treasure room.", True, (0, 255, 255))
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
        screen.blit(piece, pos)
        number = font.render(str(piece_numbers[i]), True, (255, 255, 255))
        screen.blit(number, (pos[0] + 10, pos[1] + 10))

# Draw try again message
def draw_try_again():
    text = font.render("Try Again!", True, (255, 0, 0))
    screen.blit(text, (300, 250))

# Draw puzzle complete screen
def draw_puzzle_complete():
    text = font.render("Congrats warrior! Press any key to proceed.", True, (0, 255, 0))
    
    # Get the width and height of the text
    text_rect = text.get_rect(center=(width // 2, height // 2))  # Center on the screen
    
    # Display the text at the calculated position
    screen.blit(text, text_rect)


# Main function
def main():
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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_state == treasure_room:
                    # Ensure that any piece can be selected when clicked
                    for i, pos in enumerate(positions):
                        rect = pygame.Rect(pos[0], pos[1], piece_size, piece_size)
                        if rect.collidepoint(event.pos):
                            selected_piece = i
                            offset_x = pos[0] - event.pos[0]
                            offset_y = pos[1] - event.pos[1]
                            break

            if event.type == pygame.MOUSEBUTTONUP:
                if current_state == treasure_room and selected_piece is not None:
                    correct_placement = True
                    for i, grid_pos in enumerate(grid_positions):
                        if abs(positions[selected_piece][0] - grid_pos[0]) < 50 and \
                           abs(positions[selected_piece][1] - grid_pos[1]) < 50:
                            # Place the piece on the grid
                            positions[selected_piece] = grid_pos
                            # Check if piece is placed correctly
                            if selected_piece == i:
                                solved[selected_piece] = True
                            else:
                                correct_placement = False
                            break
                    selected_piece = None

                    # If the placement is incorrect, randomize and display try again message
                    if not correct_placement:
                        positions = randomize_positions()
                        try_again = True
                        try_again_timer = pygame.time.get_ticks()

            if event.type == pygame.MOUSEMOTION:
                if current_state == treasure_room and selected_piece is not None:
                    positions[selected_piece] = (event.pos[0] + offset_x, event.pos[1] + offset_y)

        # Game flow
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
            pygame.display.flip() 
            pygame.time.delay(3000)  # Show for 3 seconds before closing
            pygame.quit()
            sys.exit()

        # Display "Try Again" message for 2 seconds if necessary
        if try_again:
            draw_try_again()
            if pygame.time.get_ticks() - try_again_timer > 2000:
                try_again = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
