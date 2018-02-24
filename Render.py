import numpy as np
from LinearAlgebra import dotProduct, crossProduct, normalize
from Transformations import Transform
import pygame, sys
from pygame.locals import *
from random import randint
from math import floor, sqrt
from numpy.linalg import inv
import datetime as dt
from Shapes import *


class Viewer():                                                        #window=(m, n, d)
    def __init__(self, pos=[0,0,0], lookAt=[0,0,-10], viewUp=[0,1,-10], window=(200, 200, 3)):
        self.pos = np.array(pos)
        self.lookAt = np.array(lookAt)
        self.viewUp = np.array(viewUp)

        self.k = self.pos - self.lookAt
        self.k = normalize(self.k)

        self.i = crossProduct(self.viewUp - self.pos, self.k)
        self.i = normalize(self.i)    

        self.j = crossProduct(self.k, self.i)

        self.worldToCamera = Transform(np.array([
            [self.i[0], self.i[1], self.i[2], -dotProduct(self.i, self.pos)], 
            [self.j[0], self.j[1], self.j[2], -dotProduct(self.j, self.pos)],
            [self.k[0], self.k[1], self.k[2], -dotProduct(self.k, self.pos)],
            [    0    ,     0    ,     0    ,                1             ]
        ]))

        self.window = window


    def status(self):
        print("pos    = " + str(self.pos))
        print("lookAt = " + str(self.lookAt))
        print("viewUp = " + str(self.viewUp))
        print("   i   = " + str(self.i))
        print("   j   = " + str(self.j))
        print("   k   = " + str(self.k))   
        print(" W->C  = \n" + str(self.worldToCamera.matrix))


class Window():

    def __init__(self, row, column, backColor=(255,255,255)):
        self.row = row
        self.column = column
        self.backColor = backColor
        self.surface = pygame.Surface((self.row, self.column))
        self.surface.fill(self.backColor)


    def display(self):
        pygame.init()

        display = pygame.display.set_mode((self.row, self.column))

        display.blit(self.surface, (0,0))
        pygame.display.flip()

        pygame.display.set_caption("Cenário com RayCasting")

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    pygame.display.update()


def Render(viewer=None, window=None, scene=None, lights=None, projection=None):
    def rayCasting(view, window, scene):
        def calcShadow(color, kR, Pin, lights):

            for li, inte in lights:
                v = Pin - np.array(li)
                v = np.append(v, 1)

                for obj in scene:
                    if isinstance(obj, Shape):
                        if intersectsAura(v, obj.aura):   
                            for k, f in enumerate(obj.faces):

                                N = crossProduct(obj(f[1])-obj(f[0]), obj(f[2])-obj(f[0]))
                                n = normalize(N)
                                
                                if dotProduct(v, n) < 0:
                                    t = dotProduct(obj(f[0]), n)/dotProduct(v, n)

                                    if t > 0:
                                        if intersectsTriangleNormal(t*v, obj, f, n):
                                            print("kr")
                                            return kR
            
            return color


        def calculateColor(lowest, lights):
            # if len(lowest) == 2:
            #     return lowest[0].colors[lowest[1]]

            if len(lowest) == 4:
                obj = lowest[0]
                k = lowest[1]
                Pin = lowest[2][:-1]
                n = lowest[3]

                V = -np.array(Pin)
                v = normalize(V)

                kR = np.array([ c/255 for c in obj.colors[k]])

                vValue = kR * np.array([.03,.03,.03])
                kr = kR * np.array([.05,.05,.05])

                for li, inte in lights:
                    L = li-Pin
                    l = normalize(L)

                    r = 2*dotProduct(l,n)*n - l

                    vValue = vValue + np.array(inte)*kR*(max(0,dotProduct(n,l)) + \
                            max(0, dotProduct(v,r)**2))

                _max = max(vValue)

                if _max > 1:
                    vValue = [round(255*v/_max) for v in vValue]
                else:
                    vValue = [round(255*v) for v in vValue]


                # vValue = calcShadow(vValue, kr, -V, lights)
                return tuple(vValue)

        def isEquals(u, v):
            for i in range(3):
                if abs(u[i]-v[i]) > 10e-5:
                    return False

            return True
        
        def intersectsAura(Pij, direct, aura):
            # t^2<Pij, Pij> - 2t<Pij, c> + <c, c> - r^2 = 0
            a = dotProduct(direct, direct)
            Pij = Pij[:-1]
            aux = Pij - np.array(aura[0])
            b = 2*dotProduct(direct, aux)
            c = dotProduct(aux, aux) - np.array(aura[1])**2

            if b**2 - 4*a*c >= 0: return True

            return False

        def intersectsTriangleNormal(Pij, obj, f, norm):
            for i in range(3):
                n1 = crossProduct(obj(f[(i+1)%3]) - obj(f[i]), Pij - obj(f[i]))
                n1 = normalize(n1)

                if not isEquals(n1, norm):
                    return False

            return True

        canvas = view.window
        scene = [viewer.worldToCamera * obj for obj in scene]

        # if projection:
        #     if projection == "ORTHO":
        #         ortho = Transform([
        #             [1, 0, 0, 0],
        #             [0, 1, 0, 0],
        #             [0, 0, 0, -canvas[2]],
        #             [0, 0, 0, 1]
        #         ])
        #         scene = [ortho * obj for obj in scene]

        print(lights)

        for li, inte in lights:
            li.append(1)

        _lights = lights
        print(_lights)
        _lights = [(np.matmul(viewer.worldToCamera.matrix, np.array(li))[:-1], inte) for li, inte in _lights]
        print(_lights)

        print("\n\nINFOS DO RAYCASTING\n")
        print("can.row = " + str(canvas[0]))
        print("can.column = " + str(canvas[1]))
        print("win.row = " + str(window.row))
        print("win.column = " + str(window.column))

        dx = canvas[0]/window.row
        dy = canvas[1]/window.column

        print("dx = w/n = " + str(dx))
        print("dy = h/m = " + str(dy))
        print("\n")
        input()

        init = dt.datetime.now()
        for i in range(window.column):
            print(chr(27) + "[2J line " + str((i+1)) + "/" + str(window.column)) 
            print(" %06.03f %%" % (100*(i+1)/window.column))
            ty = canvas[1]/2 - dy * (i + .5)
            
            for j in range(window.row):
                tx = -canvas[0]/2 + dx * (j + .5)
                Pij = np.array([tx, ty, -canvas[2], 1])

                # Pinit = np.array([tx, ty, -canvas[2], 1])

                if projection == "ORTHO":
                    D = np.array([0,0,-1,1])
                elif projection == "OBLIQ_CAVALIER":
                    D = np.array([sqrt(2)/2., sqrt(2)/2., -1, 1])
                elif projection == "OBLIQ_CABINET":
                    D = np.array([[sqrt(2)/4., sqrt(2)/4., -1, 1]])
                else:
                    D = np.array([tx, ty, -canvas[2], 1])


                lowerT = float("inf")
                lowest = None

                for obj in scene:
                    if isinstance(obj, Shape):
                        if intersectsAura(Pij, D, obj.aura):   
                            for k, f in enumerate(obj.faces):

                                N = crossProduct(obj(f[1])-obj(f[0]), obj(f[2])-obj(f[0]))
                                n = normalize(N)
                                
                                if dotProduct(Pij, n) < 0:
                                    t = dotProduct((np.array(obj(f[0]))-Pij), n)/dotProduct(D, n)

                                    if 0 <= t < lowerT:
                                        if intersectsTriangleNormal(Pij+t*D, obj, f, n):
                                            lowerT = t
                                            lowest = (obj, k, Pij+t*D, n)
                    else:
                        print("NADICA DE NADA")  

                if lowerT != float("inf") and lowest:
                    window.surface.set_at((j,i), calculateColor(lowest, _lights))

        end = dt.datetime.now()
        print(chr(27) + "[2J" + "Imagem gerada em " + str(end-init))
        
    
    rayCasting(viewer, window, scene)
    window.display()


    




