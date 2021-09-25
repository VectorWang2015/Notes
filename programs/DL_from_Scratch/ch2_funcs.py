import numpy as np
from typing import Dict, Tuple
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


batch = Tuple[np.ndarray, np.ndarray]

def forward_linear_regression(x_batch: np.ndarray,
        y_batch: np.ndarray,
        weights: Dict[str, np.ndarray]
        ) -> Tuple[float, Dict[str, np.ndarray]]:
    
    assert x_batch.shape[0] == y_batch.shape[0]
    assert x_batch.shape[1] == weights['w'].shape[0]
    assert weights['b'].shape[1] == 1 and weights['b'].shape[0] == 1

    # x -> n -> p -> loss
    n = np.dot(x_batch, weights['w'])
    p = n + weights['b']
    loss = np.mean(np.power(y_batch - p, 2))

    forward_info: Dict[str, np.ndarray] = {}
    forward_info['x'] = x_batch
    forward_info['n'] = n
    forward_info['p'] = p
    forward_info['y'] = y_batch

    return forward_info, loss


def forward_loss(X: np.ndarray,
                 y: np.ndarray,
                 weights: Dict[str, np.ndarray]) -> Tuple[Dict[str, np.ndarray], float]:
    '''
    Generate predictions and calculate loss for a step-by-step linear regression
    (used mostly during inference).
    '''
    N = np.dot(X, weights['w'])

    P = N + weights['b']

    loss = np.mean(np.power(y - P, 2))

    forward_info: Dict[str, ndarray] = {}
    forward_info['x'] = X
    forward_info['n'] = N
    forward_info['p'] = P
    forward_info['y'] = y

    return forward_info, loss


"""
x -> n -> p -> loss
  `w   +b   mean(pow())
"""
def loss_gradients(forward_info: Dict[str, np.ndarray],
        weights: Dict[str, np.ndarray]
        ) -> Dict[str, np.ndarray]:
        
    dl_dp = 2 * (forward_info['p'] - forward_info['y'])
    dp_dn = np.ones_like(forward_info['n'])
    dn_dw = np.transpose(forward_info['x'], (1,0))
    dp_db = np.ones_like(weights['b'])

    dl_db = (dl_dp * dp_db).sum(axis=0)/20

    dl_dn = dl_dp * dp_dn
    dl_dw = np.dot(dn_dw, dl_dn)

    loss_gradients: Dict[str, np.ndarray] = {}
    loss_gradients['w'] = dl_dw
    loss_gradients['b'] = dl_db

    return loss_gradients


def predict(x: np.ndarray,
        weights: Dict[str, np.ndarray]):

    n = np.dot(x, weights['w'])
    return n+weights['b']


# mean absolute error
def mae(predi: np.ndarray,
        actual: np.ndarray):
    return np.mean(np.abs(predi - actual))


# root mean square error
def rmse(predi: np.ndarray,
        actual: np.ndarray):
    return np.sqrt(np.mean(np.power(predi-actual,2)))


def to_2d_np(a: np.ndarray,
        type_: str = 'col') -> np.ndarray:
    assert a.ndim == 1, \
            "input tensor must be be 1 dimensional"

    if type_ == "col":
        return a.reshape([-1,1])
    elif type_ == "row":
        return a.reshape([1,-1])


def permute_data(x: np.ndarray,
        y: np.ndarray):
    # x.shape[0] returns length of 0-axis
    # permutation shuffles 0-9
    perm = np.random.permutation(x.shape[0])
    return x[perm], y[perm]


def generate_batch(x: np.ndarray,
        y: np.ndarray,
        start: int=0,
        batch_size: int=10) -> batch:

    assert x.ndim == y.ndim == 2, \
            "x and y must be 2d"

    if start+batch_size > x.shape[0]:
        batch_size = x.shape[0] - start

    x_batch = x[start:start+batch_size]
    y_batch = y[start:start+batch_size]

    return x_batch, y_batch


def init_weights(n_in: int) -> Dict[str, np.ndarray]:
    weights: Dict[str, np.ndarray] = {}

    w = np.random.randn(n_in, 1)
    b = np.random.randn(1, 1)

    weights['w'] = w
    weights['b'] = b

    return weights


def train(x: np.ndarray,
        y: np.ndarray,
        n_iter: int = 1000,
        learning_rate: float = 1e-2,
        batch_size: int = 100,
        return_losses: bool = False,
        return_weights: bool = False,
        seed: int = 1) -> None:

    if seed:
        np.random.seed(seed)

    losses = []

    start = 0
    # init weights
    weights = init_weights(x.shape[1])

    # permute x, y
    x, y = permute_data(x, y)

    # train
    for i in range(n_iter):
        # check start
        if start >= x.shape[0]:
            x, y = permute_data(x, y)
            start = 0

        x_batch, y_batch = generate_batch(x, y, start, batch_size)
        start +=  batch_size

        # train using generated batch
        forward_info, loss = forward_loss(x_batch, y_batch, weights)

        if return_losses:
            losses.append(loss)

        loss_grad = loss_gradients(forward_info, weights)

        for key in weights.keys():
            weights[key] -= loss_grad[key]*learning_rate

    if return_weights:
        return losses, weights

    return None


if __name__ == "__main__":
    boston = load_boston()
    data = boston['data']
    target = boston['target']
    feature_names = boston['feature_names']
    s = StandardScaler()
    data = s.fit_transform(data)

    x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.3, random_state=80718)

    y_train, y_test = y_train.reshape([-1,1]), y_test.reshape([-1,1])

    train_info = train(x_train, y_train, n_iter=1000, learning_rate=0.001, batch_size=23, return_losses=True, return_weights=True, seed=180708)
    losses, weights = train_info
    #print(losses)

    plt.plot(np.arange(1000), losses)
    plt.show()
