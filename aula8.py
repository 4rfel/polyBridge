import numpy as np
from time import time

x = 10000
#1
t0_np = time()
matrix_np = np.zeros([x, x])
t1_np = time()

t0_for = time()
matrix_for = []
for i in range(x):
    matrix_for.append([])
    for j in range(x):
        matrix_for[i].append(0)
t1_for = time()

dt_np = t1_np - t0_np
dt_for = t1_for - t0_for

print(f"numpy: {dt_np}s\nfor: {dt_for}\n")

#2
t0_np = time()
matrix_np[0,:] = 1
t1_np = time()


t0_for = time()
for i in range(x):
    matrix_for[0][i] = 1
t1_for = time()
dt2_np = t1_np - t0_np
dt2_for = t1_for - t0_for

print(f"numpy: {dt2_np}s\nfor: {dt2_for}\n")