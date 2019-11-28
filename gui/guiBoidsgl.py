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

from gui.guigl import GuiGL
from helper import util
from helper.vector2D import Vector2D

BLACK = [0, 0, 0]
WHITE = [1, 1, 1]
GREEN = [0, 1, 0]
RED = [1, 0, 0]
BLUE = [0, 0, 1]
_CHANGE_VECTOR_LENGTH = 15.0
colors = [BLACK, GREEN, RED, BLUE]


class GuiBoidsGL(GuiGL):
    def __init__(self, map):
        GuiGL.__init__(self,map)
        self.title = "GUI Boids Simulation"



    def render_agent(self, b):
        glBegin(GL_TRIANGLES)
        glColor3f(*colors[b.famille % len(colors)])
        glVertex2f(-(5), 0.0)
        glVertex2f(5, 0.0)
        glVertex2f(0.0, 5 * 3.0)
        glEnd()



