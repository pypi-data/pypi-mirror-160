import numpy as np
from math import gcd


def my_chop2(sv, eps):
    if eps <= 0.0:
        r = len(sv)
        return r
    sv0 = np.cumsum(abs(sv[::-1]) ** 2)[::-1]
    ff = [i for i in range(len(sv0)) if sv0[i] < eps ** 2]
    if len(ff) == 0:
        return len(sv)
    else:
        return np.amin(ff)

def factor(n):
    """returns all irreducible factors of x in vector
    n : int
    Returns
    -------
    T : vector
        factors
    """
    factors = []
    def get_factor(n):
        x_fixed = 2
        cycle_size = 2
        x = 2
        factor = 1
        while factor == 1:
            for count in range(cycle_size):
                if factor > 1: break
                x = (x * x + 1) % n
                factor = gcd(x - x_fixed, n)
            cycle_size *= 2
            x_fixed = x
        return factor
    while n > 1:
        next = get_factor(n)
        factors.append(next)
        n //= next
    return factors

# generate tr core tensors randomly
def init_tr_cores(tensor_size, tr_rank):
    tr_cores = []
    ndims = len(tensor_size)
    tr_rank.append(tr_rank[0])
    for n in range(0, ndims):
        tr_cores.append(0.1 * np.random.rand(tr_rank[n], tensor_size[n], tr_rank[n + 1]))
    return tr_cores

# backslash \
def backslash(a, b):
    m, n=a.shape
    p , q = b.shape
    if(m!=p):
        print('dimensions do not match!')
        return -1
    if(m==n):
        return np.linalg.solve(a, b)
    else:
        a1 = a.T.dot(a)
        b1 = a.T.dot(b)
        return np.linalg.solve(a1, b1)
# slash /
def slash(a,b):
    a=a.T
    b=b.T
    x = backslash(a,b)
    return x.T

def TR_initcoreten(T, r):
    '''

    :param T: narray
    :param r: list
    :return:
    Z: list
    '''
    S = T.shape
    N = int(np.size(S))
    # Z = np.zeros((N,), dtype=np.object)  # 设置 dtype=np.object，可以在矩阵中设置形状不同的子矩阵
    Z = []
    for i in range(N - 1):
        Z.append(np.random.randn(r[i], S[i], r[i + 1]))
    Z.append(np.random.randn(r[N - 1], S[N - 1], r[0]))

    return Z

def circshift(od):
    item = od.pop(0)
    od.append(item)
    return od

def tuple_ops(tpl, idxs):
    new_list = []
    for idx in idxs:
        new_list.append(tpl[idx])
    return new_list

def tenmat_sb(X, k):
    S = X.shape
    N = len(S)

    if k == 1:
        X_sb_k = np.reshape(X, (S[0], int(X.size / S[0])))
    elif k == N:
        X_sb_k = np.reshape(X, (int(X.size / S[N - 1]), S[N - 1]))
        X_sb_k = np.transpose(X_sb_k, (1, 0))

    else:
        X = np.reshape(X, (np.prod(S[0:k - 1]), int(X.size / np.prod(S[0:k - 1]))))
        X = np.transpose(X, [1, 0])
        X_sb_k = np.reshape(X, (S[k - 1], int(X.size / S[k - 1])))

    return X_sb_k


# formula 21 of <Tensor Ring Decomposition>
# Z is cell mode tensor cores
def TR_full_Z_k(Z, k):
    N = Z.size()


def Z_neq(Z, n):
    Z = np.roll(Z, -n - 1)  # arrange Z{n} to the last core, so we only need to multiply the first N-1 core
    N = np.size(Z, 0)
    P = Z[0]

    for i in range(N - 2):
        zl = np.reshape(P, (int(P.size / (np.size(Z[i], 2))), np.size(Z[i], 2)))
        zr = np.reshape(Z[i + 1], (np.size(Z[i + 1], 0), int(Z[i + 1].size / (np.size(Z[i + 1], 0)))))
        P = np.dot(zl, zr)
    Z_neq_out = np.reshape(P, (
    np.size(Z[0], 0), int(P.size / (np.size(Z[0], 0) * (np.size(Z[N - 1], 2)))), np.size(Z[N - 1], 2)))

    return Z_neq_out
