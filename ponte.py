from viga import Viga
import numpy as np
row = 0
col = 1

class Ponte():
    def __init__(self, vigas, quant_nos, vu, vP):
        self.vigas = vigas
        self.quant_nos = quant_nos
        self.vP = vP
        self.vu = vu

    def get_mrs(self):
        for viga in self.vigas:
            viga.get_mr()

    def mount_global_mr(self):

        Mr_global = np.zeros([self.quant_nos*2, self.quant_nos*2])
        for viga in self.vigas:
            Mr_global[viga.gdl[0]:viga.gdl[1]+1, viga.gdl[0]:viga.gdl[1]+1] += viga.mr[0:2, 0:2]
            Mr_global[viga.gdl[2]:viga.gdl[3]+1, viga.gdl[0]:viga.gdl[1]+1] += viga.mr[0:2, 2:4]
            Mr_global[viga.gdl[0]:viga.gdl[1]+1, viga.gdl[2]:viga.gdl[3]+1] += viga.mr[2:4, 0:2]
            Mr_global[viga.gdl[2]:viga.gdl[3]+1, viga.gdl[2]:viga.gdl[3]+1] += viga.mr[2:4, 2:4]
        self.Mr_global = Mr_global

    def cond_contorn(self):
        a = []
        for i in range(self.vu.shape[0]):
            if self.vu[i] == 0:
                a.append(i)
        
        self.vP = np.delete(self.vP, obj=a, axis=row)
        self.Mr_global = np.delete(self.Mr_global, obj=a, axis=row)
        self.Mr_global = np.delete(self.Mr_global, obj=a, axis=col)

    def resolve(self):
        vuf = np.linalg.solve(self.Mr_global, self.vP)
        self.vu = self.remount_vu(self.vu, vuf)

    def remount_vu(self, vu, vuf):
        v = []
        k = 0
        for i in vu:
            if i == 0:
                v.append(0)
            else:
                v.append(vuf[k])
                k += 1
        return np.array(v)

    def calc_reacao_apoio(self):
        self.mount_global_mr()
        return np.matmul(self.Mr_global, self.vu)

    def calc_deformacao_global(self, tensao=0):
        deformacoes = []
        for viga in self.vigas:
            m = np.array([-viga.c, -viga.s, viga.c, viga.s])
            vu_local_global = []
            for i in viga.gdl:
                vu_local_global.append(self.vu[i])
            vu_local_global = np.array(vu_local_global)
            if not tensao:
                d = np.matmul(m, vu_local_global)/viga.L
                viga.deformacao = d
            else:
                d = viga.E*np.matmul(m, vu_local_global)/viga.L
                viga.tensao = d
            deformacoes.append(d)

        return deformacoes

    def calc_tensao_global(self):
        return self.calc_deformacao_global(1)


# A = 2e-4    
# E = 210e9

# node1 = [  0,   0]
# node2 = [  0, 0.4]
# node3 = [0.3, 0.4]

# vu = np.array([0, 1, 0, 0, 1, 1])

# quant_nos = 3

# vP = np.array([0, 0, 0, 0, 150, -100])

# viga1 = Viga(node1, node2, A, E, [1, 2])

# viga2 = Viga(node2, node3, A, E, [2, 3])

# viga3 = Viga(node3, node1, A, E, [3, 1])

# vigas = [viga1, viga2, viga3]

# ponte = Ponte(vigas, quant_nos, vu, vP)

# ponte.get_mrs()
# ponte.mount_global_mr()
# ponte.cond_contorn()
# ponte.resolve()
# reacao = ponte.calc_reacao_apoio()
# d = ponte.calc_deformacao_global()
# t = ponte.calc_tensao_global()


# print(f"""deslocamento: 
# {ponte.vu}

# reacao:
# {reacao}

# deformacao:
# {d}

# tensao:   
# {t}
# """)


