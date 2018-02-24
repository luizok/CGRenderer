import numpy as np

class Object():
    def __init__(self, shapes, refAmb=[1,1,1], refDif=[1,1,1], refEspec=[1,1,1], m=1):
        self.shapes = shapes
        self.refAmbient = np.array(refAmb)
        self.refDifuse = np.array(refDif)
        self.refEspecular = np.array(refEspec)
        self.m = m