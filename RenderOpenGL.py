import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from Shapes import Shape
from LinearAlgebra import *
from Transformations import Transform as T
from time import sleep
from random import uniform as rand
from math import sqrt


def ObjectHandler(obj: Shape):
    
    # glMateriali(GL_FRONT, GL_SHININESS, 60)
    # glMaterialfv(GL_FRONT, GL_SPECULAR, [1,1,1,1])

    glBegin(GL_TRIANGLES)
    for i, face in enumerate(obj.faces):
        for vertex in face:
            color = [c/255 for c in obj.colors[i]]
            glColor3fv(tuple(color))
            glVertex3fv(obj[vertex][:-1])

            glMaterial(GL_FRONT, GL_AMBIENT , color)
            glMaterial(GL_FRONT, GL_DIFFUSE , color)
            glMaterial(GL_FRONT, GL_SPECULAR , color)
    glEnd()

    glBegin(GL_LINES)
    for edge in obj.edges:
        for vertex in edge:
            glVertex3fv(obj[vertex][:-1])
    glEnd()


def RenderAll(viewer, win, scene, lights):
    def display():
        glClearColor(win.backColor[0]/255, win.backColor[1]/255, win.backColor[2]/255, 0.)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        for i, obj in enumerate(scene):
            if isinstance(obj, Shape):
                ObjectHandler(obj)

            elif isinstance(obj, Object):
                for shp in obj.shapes:
                    ObjectHandler(shp)
        
        glutSwapBuffers()

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowPosition(50,100);
    glutInitWindowSize(win.row, win.column);
    glutCreateWindow("Cenário em OpenGl")

    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [.3,.3,.3])
    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_3D_COLOR)

    glShadeModel(GL_SMOOTH)
    glPolygonMode(GL_FRONT, GL_FILL)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glEnable(GL_LIGHTING)

    glLightfv(GL_LIGHT1, GL_POSITION, [0, 14, 13])
    glLightfv(GL_LIGHT1, GL_AMBIENT, [.2,.2,.2])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [.2,.2,.2])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [.3,.3,.3])
    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 1)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, 1)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0)
    glEnable(GL_LIGHT1)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(90,viewer.window[0]/viewer.window[1], viewer.window[2],100)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(
        viewer.pos[0],viewer.pos[1], viewer.pos[2],
        viewer.lookAt[0], viewer.lookAt[1], viewer.lookAt[2],
        viewer.viewUp[0], viewer.viewUp[1], viewer.viewUp[2] 
    )
    glutDisplayFunc(display)
    glutMainLoop()