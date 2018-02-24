import numpy as np
from math import sqrt
from numpy import matmul


def dist(obj=None, edge=None, p1=None, p2=None):
    if obj and edge:
        return sqrt(sum([(obj(edge[0])[i]-obj(edge[1])[i])**2 for i in range(3)]))

    if p1 and p2:
        return sqrt(sum([(p1[i]-p2[i])**2 for i in range(3)]))



def dotProduct(u, v):
    if len(u) > 3:
        u = u[:-1]

    if len(v) > 3:
        v = v[:-1]

    return np.dot(u, v)


def crossProduct(u, v):
    # def printCross(u, v):
    #     print("CROSS PRODUCT " + str(u) + " x " + str(v) + " = ")
    #     for i in range(3):
    #         print(str(u[(i+1)%3])+"*"+str(v[(i+2)%3])+" - "+str(v[(i+1)%3])+"*"+str(u[(i+2)%3])\
    #         +" = " + str(u[(i+1)%3]*v[(i+2)%3] - u[(i+2)%3]*v[(i+1)%3]))

    # printCross(u, v)
    return np.array([
        u[1]*v[2] - u[2]*v[1],
        u[2]*v[0] - u[0]*v[2],
        u[0]*v[1] - u[1]*v[0],
        0
    ])

def normalize(u):
    norm = sqrt(dotProduct(u, u))    
    v = np.append(np.array([u[i]/norm for i in range(3)]), [1])

    return v 

# def mul(matrix, obj):
#     from ObjectGenerator import Object

#     vertex = np.transpose(matmul(matrix, np.transpose(obj.vertex))).tolist()
#     names = obj.names
#     edges = obj.edges
#     faces = obj.faces

#     return Object(vertex, names, edges, faces)
