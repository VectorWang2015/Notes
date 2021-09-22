import numpy as np
from typing import Callable, List

Array_funcs = Callable[[np.ndarray], np.ndarray]
Chain = List[Array_funcs]


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
