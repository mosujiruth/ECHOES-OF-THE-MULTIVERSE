import pygame
import sys
import random
# Initialize Pygame
pygame.init()

# Screen pixels
width, height = 800, 600
puzzle_size = 400  
piece_size = puzzle_size // 2  

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

# display puzzle pic
puzzle_image = pygame.image.load('tesseract.avif')
puzzle_image = pygame.transform.scale(puzzle_image, (puzzle_size, puzzle_size))

# pecahkan the pic to 4 
pieces = [
    puzzle_image.subsurface((0, 0, piece_size, piece_size)),
    puzzle_image.subsurface((piece_size, 0, piece_size, piece_size)),
    puzzle_image.subsurface((0, piece_size, piece_size, piece_size)),
    puzzle_image.subsurface((piece_size, piece_size, piece_size, piece_size))
]

#the puzzle grids position
grid_positions = [(200, 100), (400, 100), (200, 300), (400, 300)]

#this code is to randomize the positions of the puzzle pieces everytime player opens the game
positions = [
    (random.randint(0, width - piece_size), random.randint(0, height - piece_size))
    for _ in range(4)
]

#this the variable of the puzzle
selected_piece = None
offset_x = 0
offset_y = 0

#if this happends the puzzle will solve
solved = [False, False, False, False]

#this is opening screen function
def draw_welcome_screen():
    font = pygame.font.Font(None, 38)
    text = font.render("Welcome to Asgard! Press any key to enter the treasure room.", True, (0, 255, 255))
    screen.blit(text, (15, 200))
 #this is second stage of the level
def draw_treasure_room():
    font = pygame.font.Font(None, 50)
    text = font.render("Solve the puzzle to get the Space Stone.", True, (0, 255, 255))
    screen.blit(text, (90, 30))
    
    # a square for the grid apperas
    for pos in grid_positions:
        pygame.draw.rect(screen, (255, 255, 255), (*pos, piece_size, piece_size), 3)
    
    # this is to put the correct puzzle pieces
    for i, (pos, piece) in enumerate(zip(positions, pieces)):
        screen.blit(piece, pos)  
#this is will appear when the puzzle get solved
def draw_puzzle_complete():
    font = pygame.font.Font(None, 48)
    text = font.render("Congrats warrior! Press any key to proceed.", True, (0, 255, 0))
    screen.blit(text, (50, 250))
#main fuction
def main():
    global selected_piece, offset_x, offset_y
    current_state = welcome_screen
    running = True
    #control the framerate (game runs at a consistent speed, making the gameplay smooth) 
    clock = pygame.time.Clock() 

    while running:
        screen.blit(background, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #stages of the level
            if event.type == pygame.KEYDOWN:
                if current_state == welcome_screen:
                    current_state = treasure_room
                elif current_state == puzzle_room:
                    current_state = next_level

            #if the player click the mouse this code wil run
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_state == treasure_room:
                    for i, pos in enumerate(positions):
                        #this code is for the player to not move the pieces thats alredy solved
                        if not solved[i]:  
                            rect = pygame.Rect(pos[0], pos[1], piece_size, piece_size)
                            if rect.collidepoint(event.pos):
                                selected_piece = i
                                offset_x = pos[0] - event.pos[0]
                                offset_y = pos[1] - event.pos[1]
                                break

            if event.type == pygame.MOUSEBUTTONUP:
                if current_state == treasure_room and selected_piece is not None:
                    #this code will automatically snap the piece into the grid when near
                    for i, grid_pos in enumerate(grid_positions):
                        if abs(positions[selected_piece][0] - grid_pos[0]) < 50 and \
                           abs(positions[selected_piece][1] - grid_pos[1]) < 50:
                            positions[selected_piece] = grid_pos
                            #this is for the pieces to remain visible after being placed in the grid
                            solved[selected_piece] = True 
                            break
                    selected_piece = None

            if event.type == pygame.MOUSEMOTION:
                if current_state == treasure_room and selected_piece is not None:
                    positions[selected_piece] = (event.pos[0] + offset_x, event.pos[1] + offset_y)

        # game flow
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
            pygame.time.delay(3000)#will display for 3 sec beofre closing or once merged files will redirect to next level
            pygame.quit()
            sys.exit()

        pygame.display.flip() 
        clock.tick(60)  

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
