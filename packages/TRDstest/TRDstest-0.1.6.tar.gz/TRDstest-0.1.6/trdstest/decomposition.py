import numpy as np
from math import prod
from trdstest.ops import my_chop2, factor, TR_initcoreten, circshift, tuple_ops, Z_neq, tenmat_sb
from trdstest.base import  tensor2mat, mat2tensor, init_tr_cores

def TRSVD(T, ep=1e-6):
    """returns all irreducible factors of x in vector
    T : ndarray
        d-dimensional tensor T
    ep : float
        prescribed relative error εp.
    Returns
    -------
    T : node
        Cores Zk
    r : 1D-array
        TR-ranks
    """
    n = T.shape
    d = len(n)
    node = {}
    r = np.ones((d))
    ep = ep / np.sqrt(d)

    for i in range(d - 1):
        T_ = T
        if i == 0:
            T = np.reshape(T_, (n[i], int(np.size(T_) / n[i])))
            u, s, v = np.linalg.svd(T, full_matrices=False)
            v = v.T
            # s = np.diag(s_)
            rc = my_chop2(s, np.sqrt(2) * ep * np.linalg.norm(s, 2))
            temp = np.cumprod(factor(rc))
            idx = int(np.abs(temp - np.sqrt(rc)) - 1)
            r[i + 1] = temp[idx]
            r[i] = rc / r[i + 1]
            u = u[:, 0:int(r[i] * r[i + 1])]
            u = np.reshape(u, (n[i], int(r[i + 1]), int(r[i])))
            node[i] = np.transpose(u, (2, 0, 1))
            s = s[0:int(r[i] * r[i + 1])]
            v = v[:, 0:int(r[i] * r[i + 1])]
            v = np.dot(v, np.diag(s)).T
            v = np.reshape(v, (int(r[i + 1]), int(r[i]), np.prod(n[1:])))
            T = np.transpose(v, (0, 2, 1))
        else:
            m = int(r[i] * n[i])
            T = np.reshape(T_, (m, int(np.size(T_) / m)))
            u, s, v = np.linalg.svd(T, full_matrices=False)
            v = v.T
            r1 = my_chop2(s, ep * np.linalg.norm(s, 2))
            r[i + 1] = np.maximum(r1, 1)
            u = u[:, 0:int(r[i + 1])]
            node[i] = np.reshape(u, (int(r[i]), n[i], int(r[i + 1])))
            v = v[:, 0:int(r[i + 1])]
            s = s[0:int(r[i + 1])]
            T = np.dot(v, np.diag(s))

    node[d - 1] = np.reshape(T, (int(r[d - 1]), n[d - 1], int(r[0])))

    return node, r



def tr_als(T, r, maxiter=10):
    """returns all irreducible factors of x in vector
    T : ndarray
        d-dimensional tensor T
    r : 1D-array
        predefined TR-ranks r.
    Returns
    -------
    node : 1D-array
        Cores Zk
    """
    tensor_size = T.shape
    dim = len(tensor_size)
    node = init_tr_cores(tensor_size, r)
    for i in range(maxiter):
        for n in range(1, dim+1):
            core_merge_flatten_trans = np.transpose(tensor2mat(core_merge(node, n), 2))
            G_neq_pinv = np.linalg.pinv(core_merge_flatten_trans)
            node[n-1] = mat2tensor(np.dot(tensor2mat(T, n), G_neq_pinv),2,node[n-1].shape)
    return node


# merge tr_cores EXCEPT the nth core
def core_merge(tr_cores, n):
    dim = len(tr_cores)
    tr_cores_shift = tr_cores[n:dim] + tr_cores[0:n] # shift the nth core to the last
    tr_mul = np.copy(tr_cores_shift[0])
    for i in range(dim-2):
        temp_core = np.copy(tr_cores_shift[i+1])
        zl = tr_mul.reshape(int(tr_mul.size/temp_core.shape[0]), temp_core.shape[0],  order='F').copy()
        zr = temp_core.reshape(temp_core.shape[0], temp_core.shape[1] * temp_core.shape[2],  order='F').copy()
        tr_mul = np.dot(zl, zr)
    s1 = tr_cores_shift[0].shape[0]
    s2 = tr_cores_shift[dim-2].shape[2]
    merge_neq_out = tr_mul.reshape(s1, int(tr_mul.size/(s1 * s2)), s2,  order='F').copy()
    return merge_neq_out


    # node, d, n, r = TRALS(T, ranks)

def TRALSAR(data, ep):
    c = data
    switch = 0
    n = c.shape
    n = sorted(n)
    # n = n.flatten()
    d = len(n)
    ratio = 0.01 / d
    maxit = 20

    r = [1 for i in range(d)]
    node = []
    for i in range(d - 1):
        node.append(np.random.randn(int(r[i]), int(n[i]), int(r[i + 1])).reshape(1, 1, -1))
    node.append(np.random.randn(int(r[d - 1]), int(n[d - 1]), int(r[0])).reshape(1, 1, -1))

    od = []
    for ods in range(d):
        od.append(ods)

    for it in range(maxit * d):
        if it > 0:
            np.moveaxis(c, 0, -1)
            od = circshift(od)
        c = c.reshape(n[od[0]], c.size // n[od[0]], order='F')

        b = node[od[1]]
        for k0 in range(2, d):
            j0 = od[k0]
            br0 = node[j0]
            br0 = br0.reshape(r[j0], int(br0.size // r[j0]))
            b = b.reshape(int(b.size // r[j0]), r[j0])
            b = b @ br0
        # print('n', n)
        # print('r', r)
        # print('od', od)
        b = b.reshape((r[od[0]], r[od[1]], prod(tuple_ops(n, od[1:]))), order='F')
        b = b.transpose((0, 2, 1))
        b = b.reshape((r[od[1]] * r[od[0]], prod(tuple_ops(n, od[1:]))), order='F')
        a0 = np.linalg.lstsq(b.T, c.T, rcond=None)[0].T
        err0 = np.linalg.norm(c - a0 @ b) / np.linalg.norm(c.flatten())
        a0 = a0.reshape(r[od[0]], n[od[0]], r[od[1]])
        node[od[0]] = a0.transpose((2, 0, 1))

        r[od[1]] = r[od[1]] + 1
        node_od = np.mean(node[od[1]].flatten()) + np.std(node[od[1]].flatten()) * np.random.rand(n[od[1]], r[od[2]])
        node_od = node_od.reshape(np.size(node_od, 1), 1, -1)

        temp = node[od[1]].copy()
        if r[od[1]] > node[od[1]].shape[1]:
            node[od[1]] = np.zeros((np.size(node_od, 0), r[od[1]], np.size(node_od, 2)))
        for ii in range(np.size(node_od, 0)):
            node[od[1]][ii, 0:temp.shape[1], :] = temp[ii, 0:temp.shape[1], :]
            node[od[1]][ii, r[od[1]] - 1, :] = node_od[ii, :, :]
        # node[od[1]] = np.concatenate((node[od[1]], node_od), axis=0)

        b = node[od[1]].reshape(node[od[1]].shape[0] * node[od[1]].shape[1], node[od[1]].shape[2])

        for k in range(2, d):
            j1 = od[k]
            br1 = node[j1]
            br1 = br1.reshape(r[j1], int(br1.size / r[j1]))
            b = b.reshape(int(b.size / r[j1]), r[j1])
            b = b @ br1
        b = b.reshape((r[od[0]], r[od[1]], prod(tuple_ops(n, od[1:]))), order='F')
        b = b.transpose((0, 2, 1))
        b = b.reshape((r[od[1]] * r[od[0]], prod(tuple_ops(n, od[1:]))), order='F')
        a1 = np.linalg.lstsq(b.T, c.T, rcond=None)[0].T
        err1 = np.linalg.norm(c - a1 @ b) / np.linalg.norm(c.flatten())

        if (err0 - err1) / (err0) > ratio * (err0 - ep) / (err0) and err0 > ep:
            a1 = a1.reshape((r[od[0]], n[od[0]], r[od[1]]), order='F')
            node[od[0]] = a1.transpose((2, 0, 1))
            err0 = err1
            switch = 0
        else:
            temp = node[od[1]].copy()
            node[od[1]] = np.zeros((node[od[1]].shape[0], node[od[1]].shape[1] - 1, node[od[1]].shape[2]))
            temp1 = np.delete(temp, r[od[1]] - 1, axis=1)
            node[od[1]] = temp1
            r[od[1]] = r[od[1]] - 1
            switch = 1

        s = np.linalg.norm(node[od[0]].flatten())
        node[od[0]] = node[od[0]] / s
        print('it: %d, err=%f' % (it, err0))
        if err0 < ep and it >= 2 * d and switch == 1:
            break
        c = c.reshape(sorted(n, reverse=True), order='F')
    node[od[0]] = node[od[0]] * s

    return node, r

