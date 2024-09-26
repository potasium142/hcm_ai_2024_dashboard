import numpy as np

f = np.load("./db/index_compact_2.npy")[:2]
c = np.array([19, 9])
f[:, 0] = c
print(f)
