import funcoesTermosol as ft
from ponte import Ponte
from viga import Viga
import numpy as np

nn, N, nm, Inc, nc, F, nr, R = ft.importa("entrada.xlsx")

# ft.plota(N, Inc)

quant_nos = nn

list_nodes = [[N[0][i], N[1][i]] for i in range(N.shape[0]+1)]

list_A = [i[3] for i in Inc]
list_E = [i[2] for i in Inc]
list_vigas_nodes = [[i[0], i[1]] for i in Inc]
# print(Inc)

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
d = ponte.calc_deformacao_global()
t = ponte.calc_tensao_global()

N_out = N + ponte.vu.reshape(N.shape)
ft.plota(N_out, Inc)

# print(N)
# print(ponte.vu.reshape(N.shape))

f_interna = 0
t_interna = 0

ft.geraSaida("out", reacao, ponte.vu, d, f_interna, t_interna)

# print(f"""deslocamento: 
# {ponte.vu}

# reacao:
# {reacao}

# deformacao:
# {d}

# tensao:   
# {t}
# """)

