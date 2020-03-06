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
        self.x = x
        self.y = y
        self.L = np.sqrt(x**2 + y**2)
        self.A = A
        self.E = E
        self.c = x/self.L
        self.s = y/self.L
        self.M = self.mount_M()
        self.nodes = [nodes[0]*2-2, nodes[0]*2-1, nodes[1]*2-2, nodes[1]*2-1]

    def calc_matriz_rigidez(self, M):
        return ((self.E*self.A)/self.L) * M

    def get_mr(self):
        self.mr = self.calc_matriz_rigidez(self.M)


    def mount_M(self):
        m0 = np.array([[self.c**2, self.c*self.s], [self.c*self.s, self.s**2]])
        M = np.zeros([4, 4])
        M[0:2, 0:2] += m0
        M[2:4, 0:2] -= m0
        M[2:4, 2:4] += m0
        M[0:2, 2:4] -= m0

        return M
        
    def calc_reacao_apoio(self):
        M = self.mount_M()
        mr = calc_matriz_rigidez()
        return np.matmul(mr, vu)
        
    def remount_vu(vu, vuf):
        v = []
        for i in vu:
            if i == 0:
                v.append(0)
            else:
                v.append(vuf[0])
                vuf = np.delete(vuf, obj=0, axis=0)
        return np.array(v)

# L = 2             # tamanho inicial (m)
# A = 0.02          # area (m**2)
# E = 200 * 10**9   # mudulo elasticidade 
# P = 50 * 10**3    # forca (N)

# F = np.array([0, 0, P, 0])
# vu = np.array([0, 0, 1, 1])

# p1 = [0, 0]
# p2 = [2, 0]

# viga = Viga(p1, p2, A, E, F, vu)

# viga.mount_mr()
# print(viga.mr)
# vu = viga.cond_contorno()
# reacao = viga.calc_deformacao_global()
# reacao = calc_reacao_apoio(E, A, L, vu)
# d = calc_deformacao(L, vu)
# t = calc_tensao(E, d)
#
# print(f"""deslocamento: 
# {vu}

# reacao:
# {0}

# deformacao:
# {0}

# tensao:   
# {0}
# """)

