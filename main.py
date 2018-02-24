from LinearAlgebra import *
from Shapes import *
from Render import *
from RenderOpenGL import RenderAll as OpenGL
from SceneGenerator import Generator
from Transformations import Transform as T
import numpy as np
from threading import Thread

from math import sqrt


if __name__ == "__main__":

    t = T.T(0,5,0)*Pyramid(3,2.5*sqrt(2),8)
    p = Prisma(height=5, radius=5, base=8)

    cUp = T.T(-1,6,3)*Cube(2,2,2, (0,255,255))
    c1 = T.T(2.5,0,-2.5)*Cube(5,5,5, (255,0,0))
    c2 = T.T(-2.5,0,2.5)*Cube(5,5,5, (0,255,0))
    c3 = T.T(-7.5,0,-2.5)*Cube(5,5,5, (0,0,255))
    c4 = T.T(-2.5,0,-7.5)*Cube(5,5,5, (255,255,0))
    p = T.Ry(45)*T.T(0,5,0)*Pyramid(4,2.5*sqrt(2),4, (255,0,255))

    scene = Generator()

    front = ([0,0,20], [0,0,0], [0,1,0])
    side = ([20,0,0], [0,0,0], [0,1,0])
    upper = ([0,20,0], [0,0,0], [0,0,1])

    principal = ([12,10,20], [0,0,0], [0,1,0])

    viewer = Viewer([12,10,20], [0,0,0], [0,1,0], (40, 40, 5))
    viewer.status()   

    win = Window(400, 400, (0, 51, 112))

    lights = [([0,14,13], [1, 1, 1])]

    t1 = Thread(target=Render, args=(viewer, win, scene, lights))
    t2 = Thread(target=OpenGL, args=(viewer, win, scene, lights))

    t1.start()
    t2.start()

    





