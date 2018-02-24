import numpy as np
from LinearAlgebra import normalize, crossProduct
from math import sin, cos, tan, pi, radians
from Shapes import Shape


class Transform():
    def __init__(self, matrix=None):
        self.matrix = matrix
    
    # Matriz de escala
    def S(sx=1, sy=1, sz=1):
        return Transform(np.array([[ sx , 0 , 0 , 0 ],
                        [ 0 , sy , 0 , 0 ],
                        [ 0 , 0 , sz , 0 ],
                        [ 0 , 0 , 0 ,  1 ]]))

    # Matriz de translação
    def T(tx, ty, tz):
        return Transform(np.array([[ 1 , 0 , 0 , tx ],
                        [ 0 , 1 , 0 , ty ],
                        [ 0 , 0 , 1 , tz ],
                        [ 0 , 0 , 0 ,  1 ]]))


    # Matriz de rotação no eixo x
    def Rx(t):
        t = radians(t)
        return Transform(np.array([[   1    ,    0    ,    0    ,    0    ],
                        [   0    ,  cos(t) ,  -sin(t),    0    ],
                        [   0    ,  sin(t) ,  cos(t) ,    0    ],
                        [   0    ,    0    ,    0    ,    1    ]]))


    # Matriz de rotação no eixo y
    def Ry(t):
        t = radians(t)
        return Transform(np.array([[ cos(t)  ,   0   ,   sin(t)  ,   0    ],
                        [    0    ,   1   ,     0     ,   0    ],
                        [ -sin(t) ,   0   ,   cos(t)  ,   0    ],
                        [    0    ,   0   ,     0     ,   1    ]]))


    # Matriz de rotação no eixo z
    def Rz(t):
        t = radians(t)
        return Transform(np.array([[ cos(t)  ,  -sin(t) ,  0    ,    0    ],
                        [ sin(t)  ,  cos(t)  ,  0    ,    0    ],
                        [    0    ,    0     ,  1    ,    0    ],
                        [    0    ,    0     ,  0    ,    1    ]]))


    # u = (x, y, z, 0)
    # Matriz de rotação em um eixo arbitrário
    def Ru(t, u):
        t = radians(t/2)
        u = normalize(u)


        L = np.array([[cos(t), -sin(t) * u[2], sin(t) * u[1], sin(t) * u[0]],
                    [sin(t) * u[2], cos(t), -sin(t) * u[0], sin(t) * u[1]],
                    [-sin(t) * u[1], sin(t) * u[0], cos(t), sin(t) * u[2]],
                    [-sin(t) * u[0], -sin(t) * u[1], -sin(t) * u[2], cos(t)]])

        R = np.array([[cos(t), -sin(t) * u[2], sin(t) * u[1], -sin(t) * u[0]],
                        [sin(t) * u[2], cos(t), -sin(t) * u[0], -sin(t) * u[1]],
                        [-sin(t) * u[1], sin(t) * u[0], cos(t), -sin(t) * u[2]],
                        [sin(t) * u[0], sin(t) * u[1], sin(t) * u[2], cos(t)]])


        return Transform(np.matmul(L, R))


    # a e b são os vetores que definem o plano de espelhamento
    def M(a, b):
        if isinstance(a, list): a = np.array(a)
        if isinstance(b, list): b = np.array(b)

        n = normalize(crossProduct(a, b))
        I = np.identity(4)
        N = np.array([[n[0] * n[0], n[1] * n[0], n[2] * n[0], 0],
                    [n[0] * n[1], n[1] * n[1], n[2] * n[1], 0],
                    [n[0] * n[2], n[1] * n[2], n[2] * n[2], 0],
                    [     0     ,      0     ,      0     , 0]])

        return Transform(I - 2*N)


    # surface = plano do cisalhamento, exp.: "xy" cisalhamento no plano xy na direção x
    #                                        "yx" cisalhamento no plano xy na direção y
    def Sh(t, surface):

        t = radians(t)
        coord = {"x": 0, "y": 1, "z": 2}
        C = np.identity(4)
        C[coord[surface[0]], coord[surface[1]]] = tan(t)

        return Transform(C)


    def __mul__(self, other):
        # if isinstance(other, Object):
        #     shapes = [None for _ in range(len(other.shapes))]

        #     for i, shp in enumerate(other.shapes):
        #         shapes[i] = self.__mul__(shp)

        #     return Object(shapes, other.refAmbient, other.refDifuse, other.refEspecular, other.m)

        if isinstance(other, Transform):
            return Transform(np.matmul(self.matrix, other.matrix))

        if isinstance(other, Shape):
            res = np.transpose(np.matmul(self.matrix, np.transpose(other.vertex)))
            return Shape(res, other.names, other.edges, other.faces, other.colors)


    __rmul__ = __mul__


















