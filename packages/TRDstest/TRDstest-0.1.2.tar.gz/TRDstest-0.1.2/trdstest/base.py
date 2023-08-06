import numpy as np

def unfold(T, n=0):
    """Mode-n unfolding of a tensor
    Parameters
    ----------
    T : ndarray
        Tensor to be unfolded
    n : int
        mode n to split
    Returns
    -------
    unfolded_T : ndarray
        unfolded tensor
    """
    T_= np.moveaxis(T, n, 0)
    unfolded_T = np.reshape(T_, (T.shape[n], -1))
    return unfolded_T

def fold(unfolded_T, n, shape):
    """Refolds the Mode-n unfolded tensor
    Parameters
    ----------
    unfolded_T : ndarray
    n : int
    shape : tuple or list
    Returns
    -------
    folded_T : ndarray
        Folded tensor
    """
    if type(shape) == tuple:
        T_shape = list(shape)
    else:
        T_shape = shape
    mode_dim = T_shape.pop(n)
    T_shape.insert(0, mode_dim)
    T_ = np.reshape(unfolded_T, T_shape)
    folded_T = np.moveaxis(T_, 0, n)
    return folded_T

def tensor2vec(T):
    """Vectorization of a tensor
    Parameters
    ----------
    T : ndarray
    Returns
    -------
    V : 1D-array
        vectorised tensor
    """
    V = np.ravel(T)
    return V

def vec2tensor(V, shape):
    """reshape the vectorised tensor to tensor
    Parameters
    ----------
    V : 1D-array
        vectorised tensor
    shape : tuple
        shape of tensor
    Returns
    -------
    T : ndarray
        tesnorized tensor
    """
    T = np.reshape(V, shape)
    return T

def tensor2mat(T, n):
    """Matricize a tensor
    Parameters
    ----------
    T : ndarray
    n : int
    Returns
    -------
    M : 2D-array
        Matricization of a tensor
    """
    M_ = T.transpose(np.append(np.arange(n - 1, T.ndim), np.arange(0, n - 1)))
    M = M_.reshape(T.shape[n-1], int(T.size/T.shape[n-1]), order='F').copy()
    # print("Type: %d" %(mat_type), ", Reshape at mode-%d" %(n), ", Transpose index:", arr, ", Matrix size: %u x %u" %(mat.shape[0], mat.shape[1]))
    return M

def mat2tensor(M, n, shape):
    """Reshape the "matricized tensor" to tensor
    Parameters
    ----------
    M : 2D-array
    n : int
    shape : tuple
    Returns
    -------
    T : ndarray
        tesnorized tensor
    """
    arr = np.append(int(np.prod(shape[n-1:len(shape)])), int(np.prod(shape[0:n - 1])))
    T_ = M.reshape(arr, order = 'F').transpose(1, 0).copy()
    T = T_.reshape(shape, order = 'F').copy()
    # print("The size of tensor is", output_tensor.shape)
    return T

