import numpy as np
from numpy import ndarray
from Typing import Tuple, Dict, Callable


def sigmoid(x: ndarray) -> ndarray:

    return 1 / (1+np.exp(-x))


def predict(x: ndarray,
        weights: Dict[str: ndarray]
        ) -> ndarray:

    M1 = np.dot(x, weights['W1'])
    N1 = M1 + weights['B1']
    O1 = sigmoid(N1)
    M2 = np.dot(O1, weights['W2'])
    P = M2 + weights['B2']

    return P


def forward_loss(x: ndarray,
        y: ndarray,
        weights: Dict[str: ndarray]
        ) -> Tuple[Dict[str:ndarray], float]:
    
    assert x.shape[1] == weights['W1'].shape[0], \
            "x's axis-1 should be the same shape as w1's axis-0"

    assert weights['B1'].shape[0] == weights['B1'].shape[1] == 1, \
            "B1 should be 1x1 ndarray"

    assert weights['W1'].shape[1] == weights['W2'].shape[0], \
            "w1's axis-1 should be the same shape as w2's axis-0"

    assert weights['B2'].shape[0] == weights['B2'].shape[1] == 1, \
            "B1 should be 1x1 ndarray"

    assert x.shape[0] == y.shape[0], \
            "x's axis-1 should be the same shape as y's axis-1"

    M1 = np.dot(x, weights['W1'])
    N1 = M1 + weights['B1']
    O1 = sigmoid(N1)
    M2 = np.dot(O1, weights['W2'])
    P = M2 + weights['B2']
    loss = np.mean(np.power(P-y, 2))

    forward_info: Dict[str: ndarray] = {}
    forward_info['M1'] = M1
    forward_info['N1'] = N1
    forward_info['O1'] = O1
    forward_info['M2'] = M2
    forward_info['P'] = P

    return forward_info, loss
