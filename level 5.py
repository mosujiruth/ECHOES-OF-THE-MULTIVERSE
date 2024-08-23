# Tears of Tarshni muhuthan
import pygame
#assists on exiting the program
import sys
#initialises pygame
pygame.init()
#display pixels
width, height =800, 600
puzzle_size = 400  # Assume puzzle image is 400x400 pixels
piece_size = puzzle_size // 2  
#creates screen according to the pixels above
screen = pygame.display.set_mode((width, height))
#set the pic as background
pygame.display.set_display('asgard.jpg')

#represent the stages of the level
#easier than plain string
WELCOME_SCREEN = "Welcome_to_asgard"
TREASURE_ROOM = "treasure_room"
PUZZLE_COMPLETE = "puzzle_complete"
NEXT_LEVEL = "next_level"

#main function
def main():
    current_state = "Welcome_to_asgard"
    #game runs(loop)
    running = True
    while running:
        for event in pygame.event.get():  # This is the event loop inside the main loop
            if event.type == pygame.QUIT:
                #game stops
                running = False
                #stages of level
        if current_state == WELCOME_SCREEN:
          pygame.display.set_caption("Welcome to Asgard! Press any key to use reality stone and enter the treasure room.")
        elif current_state == TREASURE_ROOM:
            pygame.display.set_caption("You are now in the treasure room. Solve the puzzle to get the Space Stone.")
            #will code for 4 jigzaw puzzle later
           #display after puzzle is complete
        elif current_state == PUZZLE_COMPLETE:
          pygame.display.set_caption("Great job soldier! your one step closer in defeating TITAN Press any key to proceed.")
           #Will merge with upcoming level
        elif current_state == NEXT_LEVEL:
            
            pygame.display.set_caption("level 6")
            pygame.display.flip()
            pygame.time.delay(3000)  # game will pause for 3 sec bfr moving to next lvl
            pygame.quit()
            sys.exit()

#as soon as the stage changes from welcom to asgard game will automatically quit
#troubleshoot will be fixed
        if current_state != "Welcome_to_asgard":

            pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()



           
           
           
           
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()



