import math
import threading
import time

import pyglet
from pyglet.gl import (
    Config,
    glEnable, glBlendFunc, glLoadIdentity, glClearColor,
    GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_COLOR_BUFFER_BIT)

from pyglet.gl import (
    glPushMatrix, glPopMatrix, glBegin, glEnd, glColor3f,
    glVertex2f, glTranslatef, glRotatef,
    GL_LINE_LOOP, GL_LINES, GL_TRIANGLES)



from pyglet.window import key
# Define some colors
BLACK = [0, 0, 0]
WHITE = [1, 1, 1]
GREEN = [0, 1, 0]
RED = [1, 0, 0]
BLUE = [0, 0, 1]
_CHANGE_VECTOR_LENGTH = 15.0
colors=[BLACK,GREEN,RED,BLUE]


class GuiBoidsGL(threading.Thread):
    def __init__(self,map):
        threading.Thread.__init__(self)
        self.printFustrum = True
        self.width = 1
        self.height=1
        self.margin = 0
        self.environment = map

    def get_window_config(self):
        platform = pyglet.window.get_platform()
        display = platform.get_default_display()
        screen = display.get_default_screen()

        template = Config(double_buffer=True, sample_buffers=1, samples=4)
        try:
            config = screen.get_best_config(template)
        except pyglet.window.NoSuchConfigException:
            template = Config()
            config = screen.get_best_config(template)

        return config

    def render_velocity(self,a):
        glColor3f(0.6, 0.6, 0.6)
        glBegin(GL_LINES)
        glVertex2f(0.0, 0.0)
        glVertex2f(0.0, a.body.fustrum.radius)
        glEnd()

    def render_view(self,a):
        glColor3f(0.6, 0.1, 0.1)
        glBegin(GL_LINE_LOOP)

        step = 10
        # render a circle for the boid's view
        for i in range(-1*a.body.fustrum.angle, a.body.fustrum.angle + step, step):
            glVertex2f(a.body.fustrum.radius * math.sin(math.radians(i)),
                       (a.body.fustrum.radius * math.cos(math.radians(i))))
        glVertex2f(0.0, 0.0)
        glEnd()



    def render_boid(self,agent):
        glBegin(GL_TRIANGLES)
        glColor3f(*colors[agent.famille % len(colors)])
        glVertex2f(-(10), 0.0)
        glVertex2f(10, 0.0)
        glVertex2f(0.0, 10 * 3.0)
        glEnd()

    def draw(self,agent, show_velocity=False, show_view=False):
        glPushMatrix()
        print(agent.body.location.toString())
        # apply the transformation for the boid
        glTranslatef(agent.body.location.x, agent.body.location.y, 0.0)


        #glRotatef(math.degrees(math.atan2(velocity[0], velocity[1])), 0.0, 0.0, -1.0)

        # render the boid's velocity
        if show_velocity:
            self.render_velocity(agent)

        # render the boid's view
        if show_view:
            self.render_view(agent)

        # render the boid itself
        self.render_boid(agent)
        glPopMatrix()


    def get_window_config(self):
        platform = pyglet.window.get_platform()
        display = platform.get_default_display()
        screen = display.get_default_screen()

        template = Config(double_buffer=True, sample_buffers=1, samples=4)
        try:
            config = screen.get_best_config(template)
        except pyglet.window.NoSuchConfigException:
            template = Config()
            config = screen.get_best_config(template)

        return config

    def run(self):
        self.run2()

    def run2(self):

        show_debug = False
        show_vectors = False
        boids = []
        attractors = []
        obstacles = []

        mouse_location = (0, 0)
        window = pyglet.window.Window(
            fullscreen=True,
            caption="Boids Simulation",
            config=self.get_window_config())

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)



        @window.event
        def on_draw():
            time.sleep(0.02)
            glClearColor(0.1, 0.1, 0.1, 1.0)
            window.clear()
            glLoadIdentity()

            for boid in  self.environment.agents:
                self.draw(boid)

            '''for attractor in attractors:
                attractor.draw()

            for obstacle in obstacles:
                obstacle.draw()'''

        @window.event
        def on_key_press(symbol, modifiers):
            if symbol == key.Q:
                self.environment.running = 0
                self.environment.raise_exception()
                self.environment.join()
                pyglet.app.exit()
            elif symbol == key.EQUAL and modifiers & key.MOD_SHIFT:
                v=0
                #boids.append(create_random_boid(window.width, window.height))
            elif symbol == key.MINUS and len(boids) > 0:
                boids.pop()
            elif symbol == key.D:
                nonlocal show_debug
                show_debug = not show_debug
            elif symbol == key.V:
                nonlocal show_vectors
                show_vectors = not show_vectors
            elif symbol == key.A:
                #attractors.append(Attractor(position=mouse_location))
                v=0
            elif symbol == key.O:
                v=0
                #obstacles.append(Obstacle(position=mouse_location))

        @window.event
        def on_mouse_drag(x, y, *args):
            nonlocal mouse_location
            mouse_location = x, y

        @window.event
        def on_mouse_motion(x, y, *args):
            nonlocal mouse_location
            mouse_location = x, y

        pyglet.app.run()

