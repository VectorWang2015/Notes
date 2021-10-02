import numpy as np

from numpy import ndarray
from typing import List


def assert_same_shape(x: ndarray, y: ndarray) -> bool:
    return x.shape == y.shape


class Operation(object):
    """
    Operation base
    """
    def __init__(self):
        pass

    def forward(self, input_: ndarray):
        """
        store input into instance, call self._output
        """
        self.input_ = input_
        self.output = self._output()
        return self.output

    def backward(self, output_grad: ndarray) -> ndarray:
        """
        call self._input_grad funcs, check if same shape
        """
        assert_same_shape(self.output, output_grad)
        self.input_grad = self._input_grad(output_grad)

        assert_same_shape(self.input_, self.input_grad)
        return self.input_grad

    def _output(self) -> ndarray:
        """
        each operation should have a _output method
        """
        raise NotImplementedError

    def _input_grad(self, output_grad: ndarray) -> ndarray:
        """
        each operation should have a _input_grad method
        """
        raise NotImplementedError


class ParamOperation(Operation):
    """
    Operation class with params
    """
    def __init__(self, param: ndarray) -> ndarray:
        """
        ParamOperation method
        """
        super().__init__()
        self.param = param

    def backward(self, output_grad: ndarray) -> ndarray:
        """
        call self._input_grad and self._param_grad, check if same shape
        """
        assert_same_shape(self.output, output_grad)

        self.input_grad = self._input_grad(output_grad)
        self.param_grad = self._param_grad(output_grad)

        assert_same_shape(self.input_, self.input_grad)
        assert_same_shape(self.param, self.param_grad)

        return self.input_grad

    def _param_grad(self, output_grad: ndarray) -> ndarray:
        """
        each ParamOperation should have _param_grad operation
        """
        raise NotImplementedError


class WeightMultiply(ParamOperation):
    def __init__(self, w: ndarray):
        super().__init__(w)

    def _output(self) -> ndarray:
        return np.dot(self.input_, self.param)

    def _input_grad(self, output_grad: ndarray) -> ndarray:
        return np.dot(output_grad, np.transpose(self.param, (1,0)))

    def _param_grad(self, output_grad: ndarray) -> ndarray:
        return np.dot(np.transpose(self.input_, (1,0)), output_grad)


class BiasAdd(ParamOperation):
    def __init__(self, b: ndarray):
        assert b.shape[0] == 1
        super().__init__(b)

    def _output(self) -> ndarray:
        return self.input_ + self.param

    def _input_grad(self, output_grad: ndarray) -> ndarray:
        return np.ones_like(self.input_) * output_grad

    def _param_grad(self, output_grad: ndarray) -> ndarray:
        param_grad = np.oneslike(self.input_) * output_grad
        # reshape necessary?
        return np.sum(param_grad, axis=0).reshape(1, param_grad.shape[1])


class Sigmoid(Operation):
    def __init__(self) -> None:
        super().__init__()

    def _output(self) -> ndarray:
        return 1.0 / (1.0 + np.exp(-1.0*self.input_))

    def _input_grad(self, output_grad: ndarray) -> ndarray:
        sigmoid_backward = self.output * (1.0 - self.output)
        return sigmoid_backward * output_grad


class Layer(object):
    def __init__(self,
            neurons: int):
        self.neurons = neurons
        self.first = True
        self.params: List[ndarray] = []
        self.param_grads: List[ndarray] = []
        self.operations: List[Operation] = []

    def _setup_layer(self, num_in: int) -> None:
        raise NotImplementedError

    def forward(self, input_: ndarray) -> ndarray:
        if self.first:
            self._setup_layer(input_)
            self.first = False

        self.input_ = input_

        for operation in self.operations:
            input_ = operation.forward(input_)

        self.output = input_

        return self.output

    def backward(self, output_grad: ndarray) -> ndarray:
        assert_same_shape(self.output, output_grad)

        for operation in reversed(self.operations):
            output_grad = operation.backward(output_grad)

        input_grad = output_grad
        self._param_grads()

        return input_grad

    def _param_grads(self) -> ndarray:
        self.param_grads = []
        for operation in self.operations:
            if issubclass(operation.__class__, ParamOperation):
                self.param_grads.append(operation.param_grad)

    def _params(self) -> ndarray:
        self.params = []
        for operation in self.operations:
            if issubclass(operation.__class__, ParamOperation):
                self.params.append(operation.param)


class Dense(Layer):
    def __init__(self,
            neurons: int,
            activation: Operation = Sigmoid()) -> None:
        super().__init__(neurons)
        self.activation = activation

    def _setup_layer(self, input_: ndarray) -> None:
        if self.seed:
            np.random.seed(self.seed)

        self.params = []

        self.params.append(np.random.randn(input_.shape[1], self.neurons))

        self.params.append(np.random.randn(1, self.neurons))

        self.operaions = [WeightMultiply(self.params[0]),
                BiasAdd(self.params[1]),
                self.activation]

        return None


class Loss(object):
    def __init__(self):
        pass

    def forward(self, prediction: ndarray, target: ndarray) -> float:
        assert_same_shape(prediction, target)

        self.prediction = prediction
        self.target = target

        loss_value = self._output()

        return loss_value

    def backward(self) -> ndarray:
        self.input_grad = self._input_grad()
        assert_same_shape(self.prediction, self.input_grad)
        return self.input_grad

    def _output(self) -> float:
        raise NotImplementedError

    def _input_grad(self) -> ndarray:
        raise NotImplementedError


class MeanSquaredError(Loss):
    def __init__(self):
        super().__init__()

    def _output(self) -> float:
        loss = np.sum(np.power(self.prediction - self.target, 2)) / self.prediction.shape[0]

        return loss

    def _input_grad(self) -> ndarray:
        return 2.0 * (self.prediction - self.target) / self.prediction.shape[0]
