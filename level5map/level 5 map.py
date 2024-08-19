# Tears of Tarshni muhuthan
import pygame
import sys
pygame.init()
width, height =800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('asgard.jpg')


WELCOME_SCREEN = "Welcome_to_asgard"
TREASURE_ROOM = "treasure_room"
PUZZLE_SOLVED = "puzzle_solved"
NEXT_LEVEL = "next_level"
def main():
    current_state = "Welcome_to_asgard"
    running = True

    while running:
        if current_state == WELCOME_SCREEN:
          print("Welcome to Asgard! Press any key to use reality stone and enter the treasure room.")
        elif current_state == TREASURE_ROOM:
            print("You are now in the treasure room. Solve the puzzle to get the Space Stone.")
            #will code for 4 jigzaw puzzle later
           #display after puzzle is complete
        elif current_state == PUZZLE_SOLVED:
           print("Great job soldier! your one step closer in defeating TITAN Press any key to proceed.")
        elif current_state == NEXT_LEVEL:
            print("level 6")
            pygame.display.flip()
            pygame.time.delay(3000)  # this will show for 3 sec
            pygame.quit()
            sys.exit()


        if current_state != "Welcome_to_asgard":

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


    
    pygame.quit()
    sys.exit()


