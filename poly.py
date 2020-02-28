import numpy as np

L = 2             # tamanho inicial (m)
A = 0.02          # area (m**2)
E = 200 * 10**9   # mudulo elasticidade 
P = 50 * 10**3    # forca (N)

def calc_matriz_rigidez(E, A, L, M, quantElementos):
    return ((E*A)/(L/quantElementos)) * M

def mount_M(F):
    m0 = np.array([[1, -1], [-1, 1]])
    M = np.zeros([len(F), len(F)])
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if(i==j and i!=M.shape[0]-1 and j!=M.shape[1]-1):
                M[i:i+2, i:i+2] += m0
    return M

def cond_contorno(F, E, A, L, vu):
    row = 0
    col = 1
    a = 0
    M = mount_M(F)
    
    for i in range(len(vu)):
        if vu[i] == 0:
            F = np.delete(F, obj=i-a, axis=row)
            M = np.delete(np.delete(M, obj=i-a, axis=row), obj=i-a, axis=col)
        a = i
    quantElementos = len(vu)-1
    mr = calc_matriz_rigidez(E, A, L, M, quantElementos)
    vu = np.linalg.solve(mr, F)
    return vu
    
def calc_reacao_apoio(E, A, L, vu):
    M = mount_M(vu)
    mr = calc_matriz_rigidez(E, A, L, M, len(vu)-1)
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

def calc_deformacao(L, vu, ):
    d = []
    for i in range(len(vu)-1):
        d.append((1/(L/(len(vu)-1)))*np.matmul(np.array([-1, 1]), np.array([vu[i], vu[i+1]])))
    d = np.array(d).reshape((len(d), 1))
    return d
        
def calc_tensao(E, d):
    return E*d


F = np.array([0, 0, P])
vu = np.array([0, 1, 1])


vuf = cond_contorno(F, E, A, L, vu)
vu = remount_vu(vu, vuf)
reacao = calc_reacao_apoio(E, A, L, vu)
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