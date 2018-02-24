import numpy as np
from LinearAlgebra import dotProduct, dist
from collections import OrderedDict
from math import sin, cos, radians
from random import randint

class Shape:            
    def __init__(self, vertex=None, vertexName=None, edges=None, faces=None, color=None):
        def calcAura(vertex):
            x_min = float("inf")
            x_max = -float("inf")
            y_min = float("inf")
            y_max = -float("inf")
            z_min = float("inf")
            z_max = -float("inf")
            
            for [x,y,z,_] in vertex:
                if x < x_min: x_min = x
                if x > x_max: x_max = x
                if y < y_min: y_min = y
                if y > y_max: y_max = y
                if z < z_min: z_min = z
                if z > z_max: z_max = z
            
            center = [(x_min + x_max)/2, (y_min + y_max)/2, (z_min + z_max)/2]
            
            return (center, dist(p1=center, p2=[x_min, y_min, z_min]))


        self.vertex = np.around(np.array(vertex), decimals=4)
        self.edges = edges
        self.faces = faces
        self.names = vertexName

        if not color:
            self.colors = [(randint(0,255), randint(0,255), randint(0,255)) for i in range(len(self.faces))]
        else:
            if isinstance(color, tuple):
                self.colors = [color for i in range(len(self.faces))]
            elif isinstance(color, list):
                self.colors = color

        if vertexName:
            self.mapVertex = OrderedDict(sorted(dict(zip(vertexName, self.vertex)).items()))
        else: self.mapVertex = {}
        self.aura = calcAura(vertex)


    def __getitem__(self, index):
        if isinstance(index, str): return self.mapVertex[index]
        if isinstance(index, int): return self.vertex[index]


    __call__ = __getitem__


    def __str__(self):
        string = "\nVÉRTICES\n"
        for key, value in self.mapVertex.items():
           string += "\'" + key + "\'" + ": " + str(value) + "\n"
        
        string += "\nARESTAS\n"
        for edge in self.edges:
            string += str(edge) + "\n" 
        
        string += "\nFACES\n"
        for face in self.faces:
            string += str(face) + "\n"

        string +="\n"

        return string        


    def status(self, printVertex=True, printEdges=False, printFaces=False):
        if printVertex and printEdges and printFaces:
            return self.__str__()
        
        if printVertex:
            string = "\nVÉRTICES\n"
            for key, value in self.mapVertex.items():
                string += "\'" + key + "\'" + ": " + str(value) + "\n"
        
        if printEdges:
            string += "\nARESTAS\n"
            for edge in self.edges:
                string += str(edge) + "\n" 
        
        if printFaces:
            string += "\nFACES\n"
            for face in self.faces:
                string += str(face) + "\n"

        string +="\n"
    
        return string


class Cube(Shape):
    def __init__(self, x=1, y=1, z=1, color=None):
        
        v = [[0, 0, 0, 1], [x, 0, 0, 1], [0, 0, z, 1], [x, 0, z, 1],
             [0, y ,0, 1], [x, y, 0, 1], [0, y, z, 1], [x, y, z, 1]]

        e = (("v0", "v1"), ("v0", "v2"), ("v0", "v4"), ("v1", "v3"), 
             ("v1", "v5"), ("v2", "v3"), ("v2", "v6"), ("v3", "v7"),
             ("v4", "v5"), ("v4", "v6"), ("v5", "v7"), ("v6", "v7"))

        f = (("v0", "v1", "v2"), ("v1", "v3", "v2"), ("v2", "v7", "v6"), 
             ("v2", "v3", "v7"), ("v3", "v5", "v7"), ("v3", "v1", "v5"),
             ("v1", "v4", "v5"), ("v1", "v0", "v4"), ("v0", "v2", "v4"),
             ("v2", "v6", "v4"), ("v4", "v6", "v5"), ("v5", "v6", "v7"))
        
        vName = ["v"+str(i) for i in range(8)]
        super(Cube, self).__init__(v, vName, e, f, color)


class Pyramid(Shape):
    def __init__(self, height=1, radius=1, base=3, color=None):

        angle = radians(360./base)
        v = []
        vName = []

        v.append([0, 0, 0, 1])
        vName.append("v0")

        for i in range(base):
            v.append([radius * cos(i*angle), 0, radius * sin(i*angle), 1])
            vName.append("v"+str(i+1))
        
        v.append([0, height, 0, 1])
        vName.append("v"+str(base+1))
        
        e = tuple([("v0", "v"+str(i)) for i in range(1, base+1)])  \
          + tuple([("v"+str(i), "v"+str(i%base + 1)) for i in range(1, base+1)]) \
          + tuple([("v"+str(i), "v"+str(base+1)) for i in range(1, base+1)])

        f = tuple([("v0", "v"+str(i), "v"+str(i%base + 1)) for i in range(1, base+1)]) \
          + tuple([("v"+str(i), "v"+str(base+1), "v"+str(i%base + 1)) for i in range(1, base+1)])


        super(Pyramid, self).__init__(v, vName, e, f, color)


class Prisma(Shape):
    def __init__(self, height=1, radius=1, base=4, color=None):

        angle = radians(360./base)
        v= []
        vName = []

        v.append([0,0,0,1])
        vName.append("v0")
        
        for i in range(base):
            v.append([radius * cos(i*angle), 0, radius * sin(i*angle), 1])   
            vName.append("v"+str(i+1)) 

        v.append([0,height,0,1])
        vName.append("v"+str(base+1))

        for i in range(base):
            v.append([radius * cos(i*angle), height, radius * sin(i*angle), 1])
            vName.append("v"+str(base+2+i))
        
        e = tuple([("v0", "v"+str(i)) for i in range(1, base+1)]) \
          + tuple([("v"+str(i), "v"+str(i%base + 1)) for i in range(1, base+1)]) \
          + tuple([("v"+str(base+1), "v"+str(base+1+i)) for i in range(1, base+1)]) \
          + tuple([("v"+str(base+1+i), "v"+str(base+1 + i%base + 1)) for i in range(1, base+1)]) \
          + tuple([("v"+str(i), "v"+str(base+1+i)) for i in range(1, base+1)])

        f = tuple([("v0", "v"+str(i), "v"+str(i%base+1)) for i in range(1, base+1)]) \
          + tuple([("v"+str(base+i%base+2), "v"+str(base+1+i), "v"+str(base+1)) for i in range(1, base+1)]) \
          + tuple([("v"+str(i%base+1), "v"+str(base+1+i), "v"+str(base+i%base+2)) for i in range(1, base+1)]) \
          + tuple([("v"+str(i), "v"+str(base+1+i), "v"+str(i%base+1)) for i in range(1, base+1)])
          

        super(Prisma, self).__init__(v, vName, e, f, color)
