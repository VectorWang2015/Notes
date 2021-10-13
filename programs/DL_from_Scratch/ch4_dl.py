from ch3_dl import *
import numpy as np


def softmax(input_: ndarray, axis: int=1) -> ndarray:
    input_base = np.sum(np.exp(input_), axis=1)
    input_base = input_base.reshape(-1,1)
    base = input_base
    return np.exp(input_) / base


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

        return np.sum(softmax_cross_entropy_loss)

    def _input_grad(self) -> ndarray:
        return self.softmax_preds - self.target


class Tanh(Operation):
    def __init__(self) -> None:
        super().__init__()

    def _output(self) -> ndarray:
        return np.tanh(self.input_)

    def _input_grad(self, output_grad: ndarray) -> ndarray:
        ones = np.oneslike(output_grad)
        return ones - np.power(np.tanh(output_grad), 2)
