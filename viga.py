import numpy as np
from math import atan, cos, sin
row = 0
col = 1

class Viga():
    def __init__(self, p1, p2, A, E, nodes):
        self.p1 = p1
        self.p2 = p2
        x = p2[0] - p1[0]
        y = p2[1] - p1[1]
        self.L = np.sqrt(x**2 + y**2)
        self.A = A
        self.E = E
        self.c = x/self.L
        self.s = y/self.L
        self.gdl = [int(nodes[0]*2-2), int(nodes[0]*2-1), int(nodes[1]*2-2), int(nodes[1]*2-1)]

    def get_mr(self):
        self.mr = ((self.E*self.A)/self.L) * self.get_M()

    def get_M(self):
        m0 = np.array([[self.c**2, self.c*self.s], [self.c*self.s, self.s**2]])
        M = np.zeros([4, 4])
        M[0:2, 0:2] += m0
        M[2:4, 0:2] -= m0
        M[2:4, 2:4] += m0
        M[0:2, 2:4] -= m0

        return M