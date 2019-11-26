import math
import threading

import pyglet
from pyglet.gl import (
    Config,
    glEnable, glBlendFunc, glLoadIdentity, glClearColor,
    GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_COLOR_BUFFER_BIT, GL_POLYGON, gl, glVertex3f)

from pyglet.gl import (
    glPushMatrix, glPopMatrix, glBegin, glEnd, glColor3f,
    glVertex2f, glTranslatef, glRotatef,
    GL_LINE_LOOP, GL_LINES, GL_TRIANGLES)

from pyglet.window import key, mouse

# Define some colors
from pyglet.window.mouse import LEFT

from helper import util
from helper.vector2D import Vector2D

BLACK = [0, 0, 0]
WHITE = [1, 1, 1]
GREEN = [0, 1, 0]
RED = [1, 0, 0]
BLUE = [0, 0, 1]
_CHANGE_VECTOR_LENGTH = 15.0
colors = [BLACK, GREEN, RED, BLUE]

line_vertex_shader = '''
    #version 330
    uniform mat4 Projection;
    in vec2 in_vert;
    in vec4 in_color;
    out vec4 v_color;
    void main() {
       gl_Position = Projection * vec4(in_vert, 0.0, 1.0);
       v_color = in_color;
    }
'''

line_fragment_shader = '''
    #version 330
    in vec4 v_color;
    out vec4 f_color;
    void main() {
        f_color = v_color;
    }
'''


class GuiBoidsGL(threading.Thread):
    def __init__(self, map):
        threading.Thread.__init__(self)
        self.printFustrum = True
        self.width = 1
        self.height = 1
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

    def run2(self):
        show_debug = False
        show_vectors = False

        mouse_location = (0, 0)
        window = pyglet.window.Window(
            fullscreen=True,
            caption="Boids Simulation")

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # window.push_handlers(pyglet.window.event.WindowEventLogger())

        def update(dt):
            self.environment.update(dt)

        # schedule world updates as often as possible
        pyglet.clock.schedule(update)

        @window.event
        def on_draw():
            glClearColor(0.1, 0.1, 0.1, 1.0)
            window.clear()
            glLoadIdentity()

            for b in self.environment.agents:
                self.drawAgent(b)

        @window.event
        def on_key_press(symbol, modifiers):
            if symbol == key.Q:
                self.environment.running = 0
                self.environment.raise_exception()
                self.environment.join()
                pyglet.app.exit()
            elif symbol == key.D:
                nonlocal show_debug
                show_debug = not show_debug
            elif symbol == key.V:
                nonlocal show_vectors
                show_vectors = not show_vectors

        @window.event
        def on_mouse_drag(x, y, *args):
            nonlocal mouse_location
            mouse_location = x, y


        @window.event
        def on_mouse_release( x, y, button, modifiers):
            nonlocal mouse_location
            print(mouse_location)

        @window.event
        def on_mouse_motion(x, y, *args):
            nonlocal mouse_location
            mouse_location = x, y
            o = self.environment.getFirstObjectByName("Attractor")
            if o is not None:
                o.location = Vector2D(x,y)

        pyglet.app.run()

    def render_velocity(self, b):
        glColor3f(0.6, 0.6, 0.6)
        glBegin(GL_LINES)
        glVertex2f(0.0, 0.0)
        glVertex2f(0.0, b.body.fustrum.radius)
        glEnd()

    def render_view(self, b):
        glColor3f(0.6, 0.1, 0.1)
        glBegin(GL_LINE_LOOP)

        step = 10
        # render a circle for the boid's view
        for i in range(-b.body.fustrum.angle, b.body.fustrum.angle + step, step):
            glVertex2f(b.body.fustrum.radius * math.sin(math.radians(i)),
                       (b.body.fustrum.radius * math.cos(math.radians(i))))
        glVertex2f(0.0, 0.0)
        glEnd()

    def render_agent(self, b):
        glBegin(GL_TRIANGLES)
        glColor3f(*colors[b.famille % len(colors)])
        glVertex2f(-(5), 0.0)
        glVertex2f(5, 0.0)
        glVertex2f(0.0, 5 * 3.0)
        glEnd()

    def drawAgent(self, b):
        glPushMatrix()
        # apply the transformation for the boid
        glTranslatef(b.body.location.x, b.body.location.y, 0.0)

        # a = signedAngle()
        glRotatef(math.degrees(math.atan2(b.body.velocity.x, b.body.velocity.y)), 0.0, 0.0, -1.0)


        # render the boid's velocity
        if False:
            self.render_velocity(b)

        # render the boid's view
        if False:
            self.render_view(b)

        # render the boid itself
        self.render_agent(b)
        glPopMatrix()


