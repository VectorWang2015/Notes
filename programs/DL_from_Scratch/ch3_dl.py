import numpy as np

from numpy import ndarray
from typing import List, Tuple

from sklearn.datasets import load_boston
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


def permute_data(X, y):
    perm = np.random.permutation(X.shape[0])
    return X[perm], y[perm]


def assert_same_shape(x: ndarray, y: ndarray) -> bool:
    return x.shape == y.shape


def to_2d_np(a: ndarray, 
          type: str="col") -> ndarray:
    '''
    Turns a 1D Tensor into 2D
    '''

    assert a.ndim == 1, \
    "Input tensors must be 1 dimensional"
    
    if type == "col":        
        return a.reshape(-1, 1)
    elif type == "row":
        return a.reshape(1, -1)


def mae(y_true: ndarray, y_pred: ndarray):
    '''
    Compute mean absolute error for a neural network.
    '''    
    return np.mean(np.abs(y_true - y_pred))


def rmse(y_true: ndarray, y_pred: ndarray):
    '''
    Compute root mean squared error for a neural network.
    '''
    return np.sqrt(np.mean(np.power(y_true - y_pred, 2)))


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
        param_grad = np.ones_like(self.input_) * output_grad
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


class Linear(Operation):
    '''
    "Identity" activation function
    '''

    def __init__(self) -> None:
        '''Pass'''        
        super().__init__()

    def _output(self) -> ndarray:
        '''Pass through'''
        return self.input_

    def _input_grad(self, output_grad: ndarray) -> ndarray:
        '''Pass through'''
        return output_grad


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
        self._params()

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
            activation: Operation = Sigmoid(),
            weight_init=None) -> None:
        super().__init__(neurons)
        self.activation = activation
        self.weight_init = weight_init

    def _setup_layer(self, input_: ndarray) -> None:
        if self.seed:
            np.random.seed(self.seed)

        if self.weight_init == "glorot":
            scale = 2 / (input_.shape[1]+self.neurons)
        else:
            scale = 1.0

        self.params = []

        self.params.append(np.random.randn(input_.shape[1], self.neurons)*scale)

        self.params.append(np.random.randn(1, self.neurons)*scale)

        self.operations = [WeightMultiply(self.params[0]),
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
    def __init__(self, normalize=False):
        super().__init__()

    def _output(self) -> float:
        loss = np.sum(np.power(self.prediction - self.target, 2)) / self.prediction.shape[0]

        return loss

    def _input_grad(self) -> ndarray:
        return 2.0 * (self.prediction - self.target) / self.prediction.shape[0]


class NeuralNetwork(object):
    def __init__(self, layers: List[Layer],
            loss: Loss,
            seed: float = 1):
        self.layers = layers
        self.loss = loss
        self.seed = seed

        if seed:
            for layer in self.layers:
                setattr(layer, "seed", self.seed)

    def forward(self, x_batch: ndarray) -> ndarray:
        x_out = x_batch
        for layer in self.layers:
            x_out = layer.forward(x_out)

        return x_out

    def backward(self, loss_grad: ndarray) -> None:
        grad = loss_grad
        for layer in reversed(self.layers):
            grad = layer.backward(grad)

        return None

    def train_batch(self,
            x_batch: ndarray,
            y_batch: ndarray) -> float:
        predictions = self.forward(x_batch)
        loss = self.loss.forward(predictions, y_batch)
        self.backward(self.loss.backward())

        return loss

    def params(self):
        for layer in self.layers:
            #print(layer)
            #print(layer.params)
            yield from layer.params

    def param_grads(self):
        for layer in self.layers:
            yield from layer.param_grads


class Optimizer(object):
    def __init__(self,
            lr: float = 0.01):
        # each optimizer has an initial learn-rate
        self.lr = lr

    def step(self) -> None:
        pass


class SGD(Optimizer):
    """
    stochastic gradient descent
    """
    def __init__(self,
            lr: float = 0.01) -> None:
        super().__init__(lr)

    def step(self):
        for (param, param_grad) in zip(self.net.params(),
                self.net.param_grads()):
            param -= self.lr * param_grad


class Trainer(object):
    def __init__(self,
            net: NeuralNetwork,
            optim: Optimizer):
        self.net = net
        self.optim = optim
        setattr(self.optim, "net", self.net)

    def generate_batches(self,
                         X: ndarray,
                         y: ndarray,
                         size: int = 32) -> Tuple[ndarray]:
        '''
        Generates batches for training 
        '''
        assert X.shape[0] == y.shape[0], \
        '''
        features and target must have the same number of rows, instead
        features has {0} and target has {1}
        '''.format(X.shape[0], y.shape[0])

        N = X.shape[0]

        for ii in range(0, N, size):
            X_batch, y_batch = X[ii:ii+size], y[ii:ii+size]

            yield X_batch, y_batch

    def fit(self, x_train: ndarray, y_train: ndarray,
            x_test: ndarray, y_test: ndarray,
            epochs: int=100,
            eval_every: int=10,
            batch_size: int=32,
            seed: int=1,
            restart: bool=True) -> None:
        np.random.seed(seed)

        if restart:
            for layer in self.net.layers:
                layer.first = True
                
        setattr(self.optim, "max_epoch", epochs)
        self.optim.setup_decay()

        for e in range(epochs):

            x_train, y_train = permute_data(x_train, y_train)

            batch_generator = self.generate_batches(x_train, y_train, batch_size)

            for ii, (x_batch, y_batch) in enumerate(batch_generator):
                self.net.train_batch(x_batch, y_batch)
                self.optim.step()

            self.optim.update_lr()

            if (e+1) % eval_every == 0:
                test_preds = self.net.forward(x_test)

                loss = self.net.loss.forward(test_preds, y_test)
                print(f"Validation loss after {e+1} epochs is {loss:.3f}")


def eval_regression_model(model: NeuralNetwork,
                          X_test: ndarray,
                          y_test: ndarray):
    '''
    Compute mae and rmse for a neural network.
    '''
    preds = model.forward(X_test)
    preds = preds.reshape(-1, 1)
    print("Mean absolute error: {:.2f}".format(mae(preds, y_test)))
    print()
    print("Root mean squared error {:.2f}".format(rmse(preds, y_test)))


if __name__ == "__main__":
    deep_neural_network = NeuralNetwork(
            layers=[Dense(neurons=13, activation=Sigmoid()),
                Dense(neurons=13, activation=Sigmoid()),
                Dense(neurons=1, activation=Linear())],
            loss=MeanSquaredError(),
            seed=20190501)

    boston = load_boston()
    data = boston.data
    target = boston.target
    features = boston.feature_names
    s = StandardScaler()
    data = s.fit_transform(data)
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.3, random_state=80718)

    # make target 2d array
    y_train, y_test = to_2d_np(y_train), to_2d_np(y_test)

    trainer = Trainer(deep_neural_network, SGD(lr=0.01))

    trainer.fit(X_train, y_train, X_test, y_test,
        epochs = 50,
        eval_every = 10,
        seed=20190501);
    print()
    eval_regression_model(deep_neural_network, X_test, y_test)
