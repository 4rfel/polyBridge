# -*- coding: utf-8 -*-
"""
A funcao 'plota' produz um gráfico da estrutura definida pela matriz de nos N 
e pela incidencia Inc.

Sugestao de uso:

from funcoesTermosol import plota
plota(N,Inc)
-------------------------------------------------------------------------------
A funcao 'importa' retorna o numero de nos [nn], a matriz dos nos [N], o numero
de membros [nm], a matriz de incidencia [Inc], o numero de cargas [nc], o vetor
carregamento [F], o numero de restricoes [nr] e o vetor de restricoes [R] 
contidos no arquivo de entrada.

Sugestao de uso:
    
from funcoesTermosol import importa
[nn,N,nm,Inc,nc,F,nr,R] = importa('entrada.xlsx')
-------------------------------------------------------------------------------
A funcao 'geraSaida' cria um arquivo nome.txt contendo as reacoes de apoio Ft, 
deslocamentos Ut, forcas Fi e tensoes Ti internas. As entradas devem ser 
vetores coluna.

Sugestao de uso:
    
from funcoesTermosol import geraSaida
geraSaida('saida',Ft,Ut,Fi,Ti)
-------------------------------------------------------------------------------

"""
def plota(N,Inc):
    # Numero de membros
    nm = len(Inc[:,0])
    
    import matplotlib as mpl
    import matplotlib.pyplot as plt

#    plt.show()
    fig = plt.figure()
    # Passa por todos os membros
    for i in range(nm):
        
        # encontra no inicial [n1] e final [n2] 
        n1 = int(Inc[i,0])
        n2 = int(Inc[i,1])        

        plt.plot([N[0,n1-1],N[0,n2-1]],[N[1,n1-1],N[1,n2-1]],color='r',linewidth=3)
        plt.plot(N[0,n1-1], N[1,n1-1], "go")
        plt.plot(N[0,n2-1], N[1,n2-1], "go")
        plt.text(N[0,n1-1]+0.01, N[1,n1-1], str(n1), fontsize=10)
        plt.text(N[0,n2-1]+0.01, N[1,n2-1], str(n2), fontsize=10)


    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.grid(True)
    plt.axis('equal')
    plt.show()

def plota_ponte(N,Inc):
    # Numero de membros
    nm = len(Inc[:,0])
    
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import numpy as np

#    plt.show()
    fig = plt.figure()

    cargax = np.array([0.19, 0.20, 0.20, 0.20, 0.21])
    cargay = np.array([0.47, 0.45, 0.51, 0.45, 0.47]) - 0.11
    plt.plot(cargax - 0.04, cargay, "g", linewidth=2)
    plt.plot(cargax + 0.04, cargay, "g", linewidth=2)

    k = 0.05
    caixax = np.array([0,          0,   0.05,  0.05,  0.45,   0.45,    0.5, 0.5, 0]) - 0.05
    caixay = np.array([0, 0.15+2*k, 0.15+2*k, 1.2*k, 1.2*k, 0.15+2*k, 0.15+2*k,   0, 0]) - 2*k

    plt.plot(caixax, caixay, "b", linewidth=2)

    # Passa por todos os membros
    for i in range(nm):
        
        # encontra no inicial [n1] e final [n2] 
        n1 = int(Inc[i,0])
        n2 = int(Inc[i,1])
        plt.plot([N[0,n1-1],N[0,n2-1]],[N[1,n1-1],N[1,n2-1]], color='r', linewidth=2)
        plt.plot(N[0,n1-1], N[1,n1-1], "go")
        plt.plot(N[0,n2-1], N[1,n2-1], "go")
        plt.text(N[0,n1-1]+0.01, N[1,n1-1], str(n1), fontsize=10)
        plt.text(N[0,n2-1]+0.01, N[1,n2-1], str(n2), fontsize=10)

    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.grid(True)
    plt.axis('equal')
    plt.show()
    
    
def importa(entradaNome):
    
    import numpy as np
    import xlrd
    
    arquivo = xlrd.open_workbook(entradaNome)
    
    ################################################## Ler os nos
    nos = arquivo.sheet_by_name('Nos')
    
    # Numero de nos
    nn = int(nos.cell(1,3).value)
                 
    # Matriz dos nós
    N = np.zeros((2,nn))
    
    for c in range(nn):
        N[0,c] = nos.cell(c+1,0).value
        N[1,c] = nos.cell(c+1,1).value
    
    ################################################## Ler a incidencia
    incid = arquivo.sheet_by_name('Incidencia')
    
    # Numero de membros
    nm = int(incid.cell(1,5).value)
                 
    # Matriz de incidencia
    Inc = np.zeros((nm,4))
    
    for c in range(nm):
        Inc[c,0] = int(incid.cell(c+1,0).value)
        Inc[c,1] = int(incid.cell(c+1,1).value)
        Inc[c,2] = incid.cell(c+1,2).value
        Inc[c,3] = incid.cell(c+1,3).value
    
    ################################################## Ler as cargas
    carg = arquivo.sheet_by_name('Carregamento')
    
    # Numero de cargas
    nc = int(carg.cell(1,4).value)
                 
    # Vetor carregamento
    F = np.zeros((nn*2,1))
    
    for c in range(nc):
        no = carg.cell(c+1,0).value
        xouy = carg.cell(c+1,1).value
        GDL = int(no*2-(2-xouy)) 
        F[GDL-1,0] = carg.cell(c+1,2).value
         
    ################################################## Ler restricoes
    restr = arquivo.sheet_by_name('Restricao')
    
    # Numero de restricoes
    nr = int(restr.cell(1,3).value)
                 
    # Vetor com os graus de liberdade restritos
    R = np.zeros((nr,1))
    
    for c in range(nr):
        no = restr.cell(c+1,0).value
        xouy = restr.cell(c+1,1).value
        GDL = no*2-(2-xouy) 
        R[c,0] = GDL-1


    return nn,N,nm,Inc,nc,F,nr,R

def geraSaida(nome,Ft,Ut,Epsi,Fi,Ti):
    with open(nome+".txt", "w") as txt:
        txt.write(f"""Reacoes de apoio [N]
{Ft}
        
Deslocamentos [m]
{Ut}
        
Deformacoes []
{Epsi}

Forcas internas [N]
{Fi}

Tensoes internas [Pa]
{Ti}""")
