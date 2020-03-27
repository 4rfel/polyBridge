from viga import Viga
import numpy as np
from time import sleep

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
        # vuf = np.linalg.solve(self.Mr_global, self.vP)
        # vuf = self.solve_jacobi()
        vuf = self.solve_gauss()
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

    def solve_gauss(self):
        # x = vu
        # B = vP
        # A = Mr_global
        vu = np.zeros(self.vP.shape)
        vu += 1
        vuj = np.copy(vu)
        tolerancia = 1e-5
        while 1:
            vu = np.copy(vuj)
            vuj = self.iteration_gauss(vuj)
            k = abs((vuj - vu) / vuj)
            if np.all(k < tolerancia):
                return vuj
            
    def iteration_gauss(self, vuj):
        for i in range(self.vP.shape[0]):
            b = self.vP[i]
            for j in range(self.vP.shape[0]):
                if i != j:
                    b -= self.Mr_global[i, j] * vuj[j]
            vuj[i] = b / self.Mr_global[i, i]

        return vuj

    def solve_jacobi(self):
        # x = vu
        # B = vP
        # A = Mr_global
        vu = np.zeros(self.vP.shape)
        vu += 1
        vuj = np.copy(vu)
        tolerancia = 1e-5
        while 1:
            vu = np.copy(vuj)
            vuj = self.iteration_gauss(vuj)
            k = abs((vuj - vu) / vuj)
            if np.all(k < tolerancia):
                return vuj

    def iteration_jacobi(self, vuj):
        vu = np.copy(vuj)
        for i in range(self.vP.shape[0]):
            b = self.vP[i]
            for j in range(self.vP.shape[0]):
                if i != j:
                    b -= self.Mr_global[i, j] * vu[j]
            vuj[i] = b / self.Mr_global[i, i]

        return vuj

    def calc_f(self, t):
        area = []
        for viga in self.vigas:
            area.append(viga.A)
        area = np.array(area)
        t = np.array(t)
        return t * area

    def testa_colapso(self, trt, trc, t, d):
        for i in t:
            if abs(i) > trt or abs(i) > trc:
                return 1
        if np.any(self.vu > 0.02):
            return 1
        # if np.any(d )
        return 0