import numpy as np
from numpy import ndarray


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
