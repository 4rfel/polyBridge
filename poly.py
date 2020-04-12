import numpy as np

def calc_matriz_rigidez(E, A, L, M, quantElementos):
    return ((E*A)/(L/quantElementos)) * M

def mount_M(F):
    m0 = np.array([[1, -1], [-1, 1]])
    M = np.zeros([len(F), len(F)])
    for i in range(M.shape[0]-1):
        M[i:i+2, i:i+2] += m0
    
    return M

def cond_contorno(F, E, A, L, vu):
    row = 0
    col = 1
    a = []
    M = mount_M(F)
    for i in range(vu.shape[0]):
        if vu[i] == 0:
            a.append(i)    
    F = np.delete(F, obj=a, axis=row)
    M = np.delete(M, obj=a, axis=row)
    M = np.delete(M, obj=a, axis=col)

    quantElementos = len(vu)-1
    mr = calc_matriz_rigidez(E, A, L, M, quantElementos)
    vu = np.linalg.solve(mr, F)
    return vu
    
def calc_reacao_apoio(E, A, L, vu, vu_orig):
    M = mount_M(vu)
    mr = calc_matriz_rigidez(E, A, L, M, len(vu)-1)
    r = np.matmul(mr, vu)
    r = np.array(r)
    for i in range(len(vu_orig)):
        if vu_orig[i] != 0:
            r[i] = 0
    return r
    
def remount_vu(vu, vuf):
    v = []
    k = 0
    for i in vu:
        if i == 0:
            v.append(0)
        else:
            v.append(vuf[k])
            k += 1;
    return np.array(v)

def calc_deformacao(L, vu, ):
    d = []
    for i in range(len(vu)-1):
        d.append((1/(L/(len(vu)-1)))*np.matmul(np.array([-1, 1]), np.array([vu[i], vu[i+1]])))
    d = np.array(d)
    return d
        
def calc_tensao(E, d):
    return E*d
    

L = 2             # tamanho inicial (m)
A = 0.02          # area (m**2)
E = 200 * 10**9   # mudulo elasticidade 
P = 50 * 10**3    # forca (N)

F = np.array([0, 0, P])
vu = np.array([0, 1, 1])
vu_orig = vu

vuf = cond_contorno(F, E, A, L, vu)
vu = remount_vu(vu, vuf)
reacao = calc_reacao_apoio(E, A, L, vu, vu_orig)
d = calc_deformacao(L, vu)
t = calc_tensao(E, d)

print(f"""deslocamento: 
{vu}

reacao:
{reacao}

deformacao:
{d}

tensao:   
{t}
""")
