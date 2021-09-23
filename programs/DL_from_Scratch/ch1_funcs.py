import numpy as np
from typing import Callable, List

Array_func = Callable[[np.ndarray], np.ndarray]
Chain = List[Array_func]


def square(x: np.ndarray) -> np.ndarray:
    """
    impose square to each element in the array
    """
    return np.power(x,2)


def leaky_relu(x: np.ndarray) -> np.ndarray:
    """
    impose leaky relu to each element in the array
    """
    return np.maximum(0.2*x, x)


def deriv(func: Callable[[np.ndarray], np.ndarray],
        input_: np.ndarray,
        delta: float = 1e-3) -> np.ndarray:
    """
    calculate derivation for given func and inputs
    """
    return (func(input_+delta)-func(input_-delta)) / (2*delta)


def chain_length_2(chain: Chain,
        x: np.ndarray) -> np.ndarray:
    """
    calculate chain funcs
    """
    assert len(chain) == 2, \
            "length of input 'chain' should be 2"

    f1 =  chain[0]
    f2 =  chain[1]

    return f2(f1(x))


def sigmoid(x: np.ndarray) -> np.ndarray:
    """
    calculate sigmoid for ndarray
    """
    return 1 / (1+np.exp(-x))


def chain_deriv_2(chain: Chain,
        x: np.ndarray) -> np.ndarray:
    """
    calculate derivation for given func chain of two
    """
    assert len(chain) == 2, \
            "This func requires a chain obj of length 2"
    assert x.ndim == 1, \
            "This func requires a 1-dimensional ndarray"

    f1 = chain[0]
    f2 = chain[1]

    df1_x = deriv(f1, x)

    f1_x = f1(x)
    df2_f1x = deriv(f2, f1_x)

    return df2_f1x * df1_x


def chain_deriv_3(chain: Chain,
        x: np.ndarray) -> np.ndarray:
    """
    calculate derivation for given func chain of three
    """
    assert len(chain) == 3, \
            "This func requires a chain obj of length 2"
    assert x.ndim == 1, \
            "This func requires a 1-dimensional ndarray"

    f1 = chain[0]
    f2 = chain[1]
    f3 = chain[2]

    df2f1_x = chain_deriv_2(np.array([f1,f2]), x)

    f2_f1_x = f2(f1(x))
    df3_f2f1x = deriv(f3, f2_f1_x)

    return df3_f2f1x * df2f1_x


def multiple_inputs_add(x: np.ndarray,
        y: np.ndarray,
        sigma: Array_func) -> np.ndarray:
    """
    add and apply sigma to ndarray x and y
    """
    assert x.shape == y.shape, \
            "x and y should be the same shape"
    return sigma(x+y)


def multiple_inputs_add_backward(x: np.ndarray,
        y: np.ndarray,
        sigma: Array_func) -> float:
    a = x+y
    ds_da = deriv(sigma, a)

    da_dx, da_dy = 1,1
    return da_dx * ds_da, da_dy * ds_da


def matmul_forward(x: np.ndarray,
        w: np.ndarray) -> np.ndarray:
    assert x.shape[1] == w.shape[0], \
            """ The num of columns for the first matrix should match
            with the num of lines for the second matrix,
            while the first matrix has {} columns with the second matrix has {} lines
            """.format(x.shape[1], w.shape[0])

    return np.dot(x,w)


def matmul_backward(x: np.ndarray,
        w: np.ndarray) -> np.ndarray:
    dn_dx = np.transpose(w, (1,0))
    return dn_dx


def matrix_forward_extra(x: np.ndarray,
        w: np.ndarray,
        sigma: Array_func) -> np.ndarray:
    assert x.shape[1] == w.shape[0]

    n = matmul_forward(x, w)

    return sigma(n)


def matrix_function_backward_1(x: np.ndarray,
        w: np.ndarray,
        sigma: Array_func) -> np.ndarray:
    assert x.shape[1] == w.shape[0]
    
    n = np.dot(x, w)
    s = sigma(n)

    ds_dn = deriv(sigma, n)
    dn_dx = matmul_backward(x, w)

    return np.dot(ds_dn, dn_dx)


def matrix_function_forward_sum(x: np.ndarray,
        w: np.ndarray,
        sigma: Array_func) -> float:
    assert x.shape[1] == w.shape[0]

    n = np.dot(x, w)
    s = sigma(n)

    return np.sum(s)


def matrix_function_backward_sum_1(x: np.ndarray,
        w: np.ndarray,
        sigma: Array_func) -> float:
    assert x.shape[1] == w.shape[0]

    n = np.dot(x, w)
    s = sigma(n)

    l = np.sum(s)

    dl_ds = np.ones_like(s)
    ds_dn = deriv(sigma, n)

    dl_dn = dl_ds * ds_dn

    dn_dx = np.transpose(w, (1,0))

    dl_dx = np.dot(ds_dn, dn_dx)

    return dl_dx
