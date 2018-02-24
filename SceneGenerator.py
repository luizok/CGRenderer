from Shapes import *
from Transformations import Transform as T

def Generator():

    chao = T.T(-100, -.1, -100)*Cube(200,.1,200, (161, 104, 61))

    casa = Cube(5, 6, 10, (227, 204, 72))
    telhado = T.T(2.3,7.5,-.2)*T.Rz(90)*T.Rx(90)*Prisma(11, 3, 3, (145, 34, 2))
    porta = T.T(1.2,0,10.1)*Cube(2, 3, .11, (255,0,0))
    janela = T.T(4.9,1,5)*Cube(.2, 3, 3, (92, 196, 202))

    poste = T.T(-1, 0, 13)*Prisma(14, .2, 10, (50,50,50))


    return [chao, porta, casa, telhado, janela, poste]


