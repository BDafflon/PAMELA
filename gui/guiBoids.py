import threading
import pygame
from environment.object import EnvironmentalObject

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
colors=[BLACK,GREEN,RED,BLUE]


class GuiBoids(threading.Thread):
    def __init__(self,map):
        threading.Thread.__init__(self)
        self.printFustrum = False
        self.width = 1
        self.height=1
        self.margin = 0
        self.environment = map

    def run(self):
        # Initialize pygame
        pygame.init()

        # Set the HEIGHT and WIDTH of the screen
        WINDOW_SIZE = [self.environment.boardW * self.width, self.environment.boardH * self.height]
        screen = pygame.display.set_mode(WINDOW_SIZE)

        # Set title of screen
        pygame.display.set_caption("Map")

        # Loop until the user clicks the close button.
        done = False

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        # -- -- -- --Main Program Loop-- -- -- -- -- -
        while not done:
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    self.environment.running = 0
                    self.environment.raise_exception()
                    self.environment.join()
                    done = True  # Flag that we are done so we exit this loop
                elif event.type == pygame.MOUSEBUTTONDOWN:  # User clicks the mouse.Get the position
                    pos = pygame.mouse.get_pos()  # Change the x / y screen coordinates to grid coordinates
                    column = pos[0] // (self.width + self.margin)
                    row = pos[1] // (self.height + self.margin)

                    print("Click ", pos, "Grid coordinates: ", row, column)
                    t = self.environment.getFirstBoid()
                    if not t == None:
                        t.body.location.x = row
                        t.body.location.y = column

            # Set the screen background
            screen.fill(WHITE)

            # Draw the grid#

            for o in self.environment.objects:
                if isinstance(o, EnvironmentalObject):
                    row = o.location.x
                    column = o.location.y

                    color = BLUE
                    pygame.draw.rect(screen, color, [column, row, 5, 5])

            for agent in self.environment.agents:
                row = int(agent.body.location.x)
                column = int(agent.body.location.y)
                if agent.type == "Boid":
                    color = colors[agent.famille % len(colors)]


                pygame.draw.rect(screen, color, [column, row , 5, 5])

                if self.printFustrum:
                    pygame.draw.circle(screen, color, [column, row], agent.body.fustrum.radius,
                                       1)  # Limit to 60 frames per second
            clock.tick(30)

            # Go ahead and update the screen with what we 've drawn.
            pygame.display.flip()

        # Be IDLE friendly.If you forget this line, the program will 'hang'#
        # on exit.
        pygame.quit()
