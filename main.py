
import pygame
from taxi import Taxi
from client import Client
from object import Destination
from object import EnvironmentalObject

import environment as env

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

PRINTFUSTRUM = False# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 5
HEIGHT = 5

# This sets the margin between each cell
MARGIN = 0
myMap = env.Environment()

myMap.addObject(Destination(50, 50))
myMap.addObject(Destination(10, 10))
myMap.addObject(Destination(90, 10))
myMap.addObject(Destination(90, 90))
myMap.addObject(Destination(10, 90))

t = Taxi()
myMap.addAgent(t)

myMap.addAgent(Taxi())

for i in range(1, 100):
    myMap.addAgent(Client())

myMap.start()

grid = []
for row in range(myMap.boardW): #Add an empty array that will hold each cell# in this row
	grid.append([])
for column in range(myMap.boardH):
    	grid[row].append(0)# Append a cell

# Set row 1, cell 5 to one.(Remember rows and# column numbers start at zero.)

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [myMap.boardW * WIDTH, myMap.boardH * HEIGHT]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Map")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -- -- -- --Main Program Loop-- -- -- -- -- -
while not done:
    for event in pygame.event.get(): #User did something
        if event.type == pygame.QUIT: #If user clicked close
            myMap.running = 0
            myMap.raise_exception()
            myMap.join()
            done = True # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN: #User clicks the mouse.Get the position
            pos = pygame.mouse.get_pos()# Change the x / y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
           
            print("Click ", pos, "Grid coordinates: ", row, column)
            t.body.location.x = row
            t.body.location.y = column

	# Set the screen background
    screen.fill(WHITE)

	# Draw the grid#
	 
    for o in myMap.objects:
        if isinstance(o, EnvironmentalObject):
            row = o.location.x
            column = o.location.y
            if o.type == "Destination":
                color = BLUE
            pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])

    for agent in myMap.agents:
        row = int(agent.body.location.x)
        column = int(agent.body.location.y)
        if agent.type == "Client":
            color = GREEN
            if agent.onboard == 1:
                continue
        if agent.type == "Taxi":
            color = BLACK
        pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])

        if PRINTFUSTRUM:
            pygame.draw.circle(screen, color, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN], agent.body.fustrum.radius * WIDTH, 1)# Limit to 60 frames per second
    clock.tick(60)

	# Go ahead and update the screen with what we 've drawn.
    pygame.display.flip()

# Be IDLE friendly.If you forget this line, the program will 'hang'#
#on exit.
pygame.quit()
