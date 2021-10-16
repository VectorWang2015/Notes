import numpy as np
import matplotlib.pyplot as plt
from lincoln.utils import mnist
from lincoln.losses import SoftmaxCrossEntropy
#from lincoln.activations import Tanh
from scipy.special import logsumexp

from ch3_dl import *


def img_show(img):
    plt.imshow(img)
    plt.show()


def softmax(input_: ndarray, axis=None) -> ndarray:
    """
    input_base = np.sum(np.exp(input_), axis=1)
    input_base = input_base.reshape(-1,1)
    base = input_base
    return np.exp(input_) / base
    """
    return np.exp(input_ - logsumexp(input_, axis=axis, keepdims=True))

class SoftmaxCrossEntropyLoss(Loss):
    def __init__(self, eps: float=1e-9):
        super().__init__()
        self.eps = eps
        self.single_output = False

    def _output(self) -> float:
        softmax_preds = softmax(self.prediction, axis=1)
        self.softmax_preds = np.clip(softmax_preds, self.eps, 1-self.eps)
        softmax_cross_entropy_loss = (
                -1.0 * self.target * np.log(self.softmax_preds) - \
                    (1.0 - self.target) * np.log(1-self.softmax_preds)
        )

        return np.sum(softmax_cross_entropy_loss) / self.prediction.shape[0]

    def _input_grad(self) -> ndarray:
        return (self.softmax_preds - self.target) / self.prediction.shape[0]


class SoftmaxCrossEntropyLoss(Loss):
    def __init__(self, eps: float=1e-9) -> None:
        super().__init__()
        self.eps = eps
        self.single_class = False

    def _output(self) -> float:

        # if the network is just outputting probabilities
        # of just belonging to one class:
        if self.target.shape[1] == 0:
            self.single_class = True

        # if "single_class", apply the "normalize" operation defined above:
        if self.single_class:
            self.prediction, self.target = \
            normalize(self.prediction), normalize(self.target)

        # applying the softmax function to each row (observation)
        softmax_preds = softmax(self.prediction, axis=1)

        # clipping the softmax output to prevent numeric instability
        self.softmax_preds = np.clip(softmax_preds, self.eps, 1 - self.eps)

        # actual loss computation
        softmax_cross_entropy_loss = (
            -1.0 * self.target * np.log(self.softmax_preds) - \
                (1.0 - self.target) * np.log(1 - self.softmax_preds)
        )

        return np.sum(softmax_cross_entropy_loss) / self.prediction.shape[0]

    def _input_grad(self) -> ndarray:

        # if "single_class", "un-normalize" probabilities before returning gradient:
        if self.single_class:
            return unnormalize(self.softmax_preds - self.target)
        else:
            return (self.softmax_preds - self.target) / self.prediction.shape[0]


class Tanh(Operation):
    def __init__(self) -> None:
        super().__init__()

    def _output(self) -> ndarray:
        return np.tanh(self.input_)

    def _input_grad(self, output_grad: ndarray) -> ndarray:
        return (1 - np.power(self.output, 2)) * output_grad


class SGDmomentum(Optimizer):
    def __init__(self,
            lr: float=0.01,
            momentum: float=0.9,
            final_lr: float=0.005,
            decay_type = None):
        super().__init__()
        self.lr = lr
        self.final_lr = final_lr
        self.momentum = momentum
        self.decay_type = decay_type
        self.first = True

    def setup_decay(self):
        if not self.decay_type:
            return
        elif self.decay_type == "exponential":
            self.decay_per_epoch = np.power((self.final_lr/self.lr), 1 / (self.max_epoch-1))
        elif self.decay_type == "linear":
            self.decay_per_epoch = (self.lr-self.final_lr) / (self.max_epoch-1)

    def update_lr(self):
        if not self.decay_type:
            return
        elif self.decay_type == "exponential":
            self.lr *= self.decay_per_epoch
        elif self.decay_type == "linear":
            self.lr -= self.decay_per_epoch

    def step(self) -> None:
        if self.first:
            self.velocities = [np.zeros_like(param)
                    for param in self.net.params()]
            self.first = False

        for (param, param_grad, velocity) in zip(self.net.params(),
                self.net.param_grads(),
                self.velocities):
            self._update_rule(param=param,
                    grad=param_grad,
                    velocity=velocity)

    def _update_rule(self, **kwargs) -> None:
        kwargs['velocity'] *= self.momentum
        kwargs['velocity'] += self.lr * kwargs['grad']

        kwargs['param'] -= kwargs['velocity']


def calc_accuracy_model(model, test_set):
    return print(f'''The model validation accuracy is: {np.equal(np.argmax(model.forward(test_set, inference=True), axis=1), y_test).sum() * 100.0 / test_set.shape[0]:.2f}%''')


# Cuz the book doesn't provide a workable code for getting mnist
# the main func here is not workable
if __name__ == "__main__":
    # mnist.init()
    x_train, y_train, x_test, y_test = mnist.load()
    # img_show(x_train[1].reshape(28,28))
    x_train, x_test = x_train-np.mean(x_train), x_test-np.mean(x_train)
    x_train, x_test = x_train/np.std(x_train), x_test/np.std(x_train)

    # one-hot encoding
    num_labels = len(y_train)
    train_labels = np.zeros((num_labels, 10))
    for i in range(num_labels):
        train_labels[i][y_train[i]] = 1

    num_labels = len(y_test)
    test_labels = np.zeros((num_labels, 10))
    for i in range(num_labels):
        test_labels[i][y_test[i]] = 1

    model = NeuralNetwork(
    layers=[Dense(neurons=89,
                  activation=Tanh(),
                  weight_init="glorot"),
            Dense(neurons=10,
                  activation=Linear(),
                  weight_init="glorot")],
            loss = SoftmaxCrossEntropyLoss(),
seed=20190119)

    optim = SGDmomentum(0.2, 0.9, final_lr=0.05, decay_type="exponential")
    trainer = Trainer(model, optim)
    trainer.fit(x_train, train_labels, x_test, test_labels,
            epochs = 50,
            eval_every = 10,
            seed=20190119,
            batch_size=60);
    print()
    #calc_accuracy_model(model, x_test)
