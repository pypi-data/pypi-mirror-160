import numpy as np
# from decomposition import TRSVD
# from decomposition import TRALS
from decomposition import TRALSAR



T = np.random.rand(3,4,5,6)
ep = 1e-5
tau = 1e-4
epoch = 20
#
# node1, r1 = TRSVD(T, ep=1e-6)
# node2, r2 = TRALS(T, tol=1e-6)
node3, r3 = TRALSAR(T, ep=1e-6)