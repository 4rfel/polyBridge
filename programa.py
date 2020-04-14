import funcoesTermosol as ft
from ponte import Ponte
from viga import Viga
import numpy as np

p = 0
nn, N, nm, Inc, nc, F, nr, R = ft.importa("ponte_imortal.xlsx")
if p:
    ft.plota_ponte(N, Inc)  

quant_nos = nn
list_nodes = [[N[0][i], N[1][i]] for i in range(N.shape[1])]
list_A = [i[3] for i in Inc]
list_E = [i[2] for i in Inc]
list_vigas_nodes = [[i[0], i[1]] for i in Inc]

vu_excel = np.array([(R[i][0]) for i in range(R.shape[0])])
vP = [F[i][0] for i in range(F.shape[0])]

vu = np.zeros(len(vP)) + 1
for i in vu_excel:
    vu[int(i)] = 0

vigas = []
for i in range(len(list_vigas_nodes)):
    viga = Viga(list_nodes[int(list_vigas_nodes[i][0]-1)], list_nodes[int(list_vigas_nodes[i][1]-1)], list_A[i], list_E[i], list_vigas_nodes[i])
    vigas.append(viga)

ponte = Ponte(vigas, quant_nos, vu, vP)

ponte.get_mrs()
ponte.mount_global_mr()
ponte.cond_contorn()
ponte.resolve()
reacao = ponte.calc_reacao_apoio()
d = np.array(ponte.calc_deformacao_global())
t = np.array(ponte.calc_tensao_global())

N_out = N + ponte.vu.reshape(N.shape)

if p:
    ft.plota_ponte(N_out, Inc)

f_interna = ponte.calc_f(t)

tensao_ruptura_tracao = 18e6
tensao_ruptura_compressao = 18e6

c = ponte.testa_colapso(tensao_ruptura_tracao, tensao_ruptura_compressao, t, d, vu, ponte.vu)
print(c)
print(ponte.calc_peso(848))
ft.geraSaida("ponte_imortal", reacao.reshape([len(reacao), 1]), ponte.vu.reshape([len(ponte.vu), 1]), d.reshape([len(d), 1]), f_interna.reshape([len(f_interna), 1]), t.reshape([len(t), 1]))

