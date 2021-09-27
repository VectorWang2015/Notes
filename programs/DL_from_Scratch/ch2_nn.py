import numpy as np
from numpy import ndarray
from typing import Tuple, Dict
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

np.set_printoptions(precision=4)
batch = Tuple[ndarray, ndarray]


def sigmoid(x: ndarray) -> ndarray:

    return 1 / (1+np.exp(-x))


def predict(x: ndarray,
        weights: Dict[str, ndarray]
        ) -> ndarray:

    M1 = np.dot(x, weights['W1'])
    N1 = M1 + weights['B1']
    O1 = sigmoid(N1)
    M2 = np.dot(O1, weights['W2'])
    P = M2 + weights['B2']

    return P


def forward_loss(x: ndarray,
        y: ndarray,
        weights: Dict[str, ndarray]
        ) -> Tuple[Dict[str,ndarray], float]:
    
    assert x.shape[1] == weights['W1'].shape[0], \
            "x's axis-1 should be the same shape as w1's axis-0"

    assert weights['W1'].shape[1] == weights['W2'].shape[0], \
            "w1's axis-1 should be the same shape as w2's axis-0"

    assert weights['B2'].shape[0] == weights['B2'].shape[1] == 1, \
            "B1 should be 1x1 ndarray"

    assert x.shape[0] == y.shape[0], \
            "x's axis-1 should be the same shape as y's axis-1"

    """
    print(weights['W1'])
    print(weights['W2'])
    print(weights['B1'])
    print(weights['B2'])
    input()
    """
    M1 = np.dot(x, weights['W1'])
    N1 = M1 + weights['B1']
    O1 = sigmoid(N1)
    M2 = np.dot(O1, weights['W2'])
    P = M2 + weights['B2']
    loss = np.mean(np.power(P-y, 2))

    forward_info: Dict[str, ndarray] = {}
    forward_info['X'] = x
    forward_info['M1'] = M1
    forward_info['N1'] = N1
    forward_info['O1'] = O1
    forward_info['M2'] = M2
    forward_info['P'] = P
    forward_info['Y'] = y

    return forward_info, loss


def loss_gradients(forward_info: Dict[str, ndarray],
        weights: Dict[str, ndarray]
        ) -> Dict[str, ndarray]:

    dl_dp = (forward_info['P'] - forward_info['Y'])
    dp_dm2 = np.ones_like(forward_info['M2'])
    dl_dm2 = dl_dp * dp_dm2

    dl_do1 = np.dot(dl_dm2, np.transpose(weights['W2'], (1,0)))
    dl_dw2 = np.dot(np.transpose(forward_info['O1'], (1,0)), dl_dm2)

    do1_dn1 = sigmoid(forward_info['N1'])*(np.ones_like(forward_info['N1']) - sigmoid(forward_info['N1']))
    dn1_dm1 = np.ones_like(forward_info['N1'])
    do1_dm1 = do1_dn1 * dn1_dm1

    dl_dn1 = dl_do1 * do1_dn1
    dl_dm1 = dl_do1 * do1_dm1
    dl_dw1 = np.dot(np.transpose(forward_info['X'], (1,0)), dl_dm1)
    
    dp_db2 = np.ones_like(weights['B2'])
    dn1_db1 = np.ones_like(weights['B1'])
    dl_db2 = (dl_dp*dp_db2).sum(axis=0)
    dl_db1 = (dl_dn1*dn1_db1).sum(axis=0)
    #print(dl_db2)
    #print(dl_db1)

    loss_gradients: Dict[str, ndarray] = {}
    loss_gradients['B1'] = dl_db1
    loss_gradients['B2'] = dl_db2
    loss_gradients['W1'] = dl_dw1
    loss_gradients['W2'] = dl_dw2

    return loss_gradients


# mean absolute error
def mae(predi: ndarray,
        actual: ndarray):
    return np.mean(np.abs(predi - actual))


# root mean square error
def rmse(predi: ndarray,
        actual: ndarray):
    return np.sqrt(np.mean(np.power(predi-actual,2)))


def to_2d_np(a: ndarray,
        type_: str = 'col') -> ndarray:
    assert a.ndim == 1, \
            "input tensor must be be 1 dimensional"

    if type_ == "col":
        return a.reshape([-1,1])
    elif type_ == "row":
        return a.reshape([1,-1])


def permute_data(x: ndarray,
        y: ndarray):
    # x.shape[0] returns length of 0-axis
    # permutation shuffles 0-9
    perm = np.random.permutation(x.shape[0])
    return x[perm], y[perm]


def generate_batch(x: ndarray,
        y: ndarray,
        start: int=0,
        batch_size: int=10) -> batch:

    assert x.ndim == y.ndim == 2, \
            "x and y must be 2d"

    if start+batch_size > x.shape[0]:
        batch_size = x.shape[0] - start

    x_batch = x[start:start+batch_size]
    y_batch = y[start:start+batch_size]

    return x_batch, y_batch


def init_weights(n_in: int, n_ns: int) -> Dict[str, ndarray]:
    weights: Dict[str, ndarray] = {}

    w1 = np.random.randn(n_in, n_ns)
    w2 = np.random.randn(n_ns, 1)
    b1 = np.random.randn(1, n_ns)
    b2 = np.random.randn(1, 1)

    weights['W1'] = w1
    weights['W2'] = w2
    weights['B1'] = b1
    weights['B2'] = b2

    return weights


def train(x: ndarray,
        y: ndarray,
        n_iter: int = 1000,
        test_every: int = 1000,
        learning_rate: float = 1e-2,
        hidden_size: int = 13,
        batch_size: int = 100,
        return_losses: bool = False,
        return_weights: bool = False,
        return_scores: bool = False,
        seed: int = 1) -> None:

    if seed:
        np.random.seed(seed)

    losses = []

    start = 0
    # init weights
    weights = init_weights(x.shape[1], hidden_size)

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

    train_info = train(x_train, y_train, n_iter=10000, learning_rate=0.001,hidden_size=13, batch_size=23, return_losses=True, return_weights=True, seed=180807)
    losses, weights = train_info
    #print(losses)

    predis = predict(x_test, weights)
    print("Mean absolute error: {}".format(round(mae(predis, y_test), 4)))
    print("Root mean square error: {}".format(round(rmse(predis, y_test), 4)))

    """
    # for plotting losses
    plt.plot(np.arange(10000), losses)
    plt.show()
    """

    """
    # for plotting predicted vs actual
    plt.xlabel("aredicted")
    plt.ylabel("Acutal")
    plt.title("Predicted vs Actual value for\ncustom linear regression model")
    plt.xlim([0,51])
    plt.ylim([0,51])
    plt.scatter(predis, y_test)
    plt.plot([0,51], [0,51])
    plt.show()
    """

    """
    for plotting most important feature vs target&prediction
    """
    NUM = 40
    a = np.repeat(x_test[:,:-1].mean(axis=0,keepdims=True), NUM, axis=0)
    b = np.linspace(-1.5, 3.5, NUM).reshape(NUM, 1)

    test_feature = np.concatenate([a, b], axis=1)
    test_predis = predict(test_feature, weights)[:,0]

    plt.scatter(x_test[:, 12], y_test)
    plt.plot(test_feature[:,-1], test_predis, linewidth=2, c='orange')
    plt.ylim([6, 51])
    plt.xlabel("Most important feature (normalized)")
    plt.ylabel("Target/Predictions")
    plt.title("Most important feature vs. target and predictions,\n custom linear regression");
    plt.show()
