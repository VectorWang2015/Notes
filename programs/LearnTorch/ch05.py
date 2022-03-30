import torch
import torch.optim as optim
from matplotlib import pyplot as plt

t_c = [0.5, 14.0, 15.0, 28.0, 11.0, 8.0, 3.0, -4.0, 6.0, 13.0, 21.0]
t_u = [35.7, 55.9, 58.2, 81.9, 56.3, 48.9, 33.9, 21.8, 48.4, 60.4, 68.4]

t_c = torch.tensor(t_c)
t_u = torch.tensor(t_u)


def model(t_u, w, b):
    return w*t_u + b


# MSE mean square err
def loss_fn(t_p, t_c):
    squared_diffs = (t_p - t_c) ** 2
    return squared_diffs.mean()


# inits, w & b are 0-axis tensors
w = torch.ones(())
b = torch.zeros(())

t_p = model(t_u, w, b)
loss = loss_fn(t_p, t_c)
print(t_p, loss)


delta = 0.1
learning_rate = 1e-2

loss_rate_change_of_w = (loss_fn(model(t_u, w+delta, b), t_c) -
        loss_fn(model(t_u, w-delta, b), t_c)) / (2.0 * delta)
w = w - learning_rate*loss_rate_change_of_w

loss_rate_change_of_b = (loss_fn(model(t_u, w, b+delta), t_c) -
        loss_fn(model(t_u, w, b-delta), t_c)) / (2.0 * delta)
b = b - learning_rate*loss_rate_change_of_b


def dloss_fn(t_p, t_c):
    dsq_diffs = 2 * (t_p - t_c)
    return dsq_diffs / t_p.size(0)


def dmodel_dw(t_u, w, b):
    return t_u


def dmodel_db(t_u, w, b):
    return 1.0


def grad_fn(t_u, t_c, t_p, w, b):
    dloss_dtp = dloss_fn(t_p, t_c)
    dloss_dw = dloss_dtp * dmodel_dw(t_u, w, b)
    dloss_db = dloss_dtp * dmodel_db(t_u, w, b)
    return torch.stack([dloss_dw.sum(), dloss_db.sum()])


def training_loop(n_epochs, learning_rate, params, t_u, t_c, print_params = True):
    for epoch in range(1, n_epochs + 1):
        w, b = params
        t_p = model(t_u, w, b)
        loss = loss_fn(t_p, t_c)
        grad = grad_fn(t_u, t_c, t_p, w, b)
        params = params - learning_rate * grad
        print("Epoch {}: Loss {}".format(epoch, float(loss)))
        if (print_params):
            print("\tParams: ", params)
            print("\tGrad: ", grad)
    return params

# normalization
t_un = t_u * 0.1

"""
params = training_loop(n_epochs=5000,
        learning_rate=1e-2,
        params=torch.tensor([1.0, 0.0]),
        t_u=t_un,
        t_c=t_c)
"""

#params = torch.tensor([1.0, 0.0], requires_grad = True)
"""
loss = loss_fn(model(t_u, *params), t_c)
loss.backward()
print(params.grad)
"""


def training_loop2(n_epochs, learning_rate, params, t_u, t_c, print_params = True):
    for epoch in range(1, n_epochs+1):
        if params.grad is not None:
            params.grad.zero_()
        loss = loss_fn(model(t_u, *params), t_c)
        loss.backward()
        grad = params.grad
        with torch.no_grad():
            params -= grad * learning_rate
        print("Epoch {}: Loss {}".format(epoch, float(loss)))
        if (print_params):
            print("\tParams: ", params)
            print("\tGrad: ", grad)
    return params

#params = training_loop(5000, 1e-2, params, t_un, t_c, print_params=True)


def training_loop3(n_epochs, optimizer, params, t_u, t_c):
    for epoch in range(1, n_epochs+1):
        t_p = model(t_u, *params)
        loss = loss_fn(t_p, t_c)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if epoch % 500 == 0:
            print("Epoch {}, Loss {}".format(epoch, loss))
    return params

"""
params = torch.tensor([1.0,0.0], requires_grad=True)
optimizer = optim.SGD([params], lr=1e-2)
params = training_loop3(5000, optimizer, params, t_un, t_c)
"""

# take 80% as train set
n_samples = t_u.shape[0]
n_val = int(0.2 * n_samples)
shuffled_indices = torch.randperm(n_samples)
train_indices = shuffled_indices[:-n_val]
val_indices = shuffled_indices[-n_val:]
print(train_indices, val_indices)

train_t_u = t_u[train_indices]
train_t_c = t_c[train_indices]
val_t_u = t_u[val_indices]
val_t_c = t_c[val_indices]

train_t_un = 0.1 * train_t_u
val_t_un = 0.1 * val_t_u


def training_loop4(n_epochs, optimizer, params, train_t_u, val_t_u, train_t_c, val_t_c):
    for epoch in range(1, n_epochs+1):
        train_t_p = model(train_t_u, *params)
        train_loss = loss_fn(train_t_p, train_t_c)

        optimizer.zero_grad()
        train_loss.backward()
        optimizer.step()

        if epoch <=3 or epoch % 500 == 0:
            with torch.no_grad():
                val_loss = loss_fn(model(val_t_u, *params), val_t_c)
                assert val_loss.requires_grad == False
            print(f"Epoch {epoch}, Training loss {train_loss.item():.4f}",f"Validation loss {val_loss.item():.4f}")

    return params


def calc_forward(t_u, t_c, is_train):
    with torch.set_grad_enabled(is_train):
        t_p = model(t_u, *params)
        loss = loss_fn(t_p, t_c)
    return loss


params = torch.tensor([1.0, 0.0], requires_grad=True)
learning_rate = 1e-2
optimizer = optim.SGD([params], lr=learning_rate)

params = training_loop4(n_epochs=5000,
        optimizer=optimizer,
        params=params,
        train_t_u=train_t_un,
        val_t_u=val_t_un,
        train_t_c=train_t_c,
        val_t_c=val_t_c)

t_p = model(t_un, *params)
fig = plt.figure(dpi=100)
plt.xlabel("Temperature (Fahrenheit)")
plt.ylabel("Temperature (Celsius)")
plt.plot(t_u.numpy(), t_p.detach().numpy())
# o for round points
plt.plot(t_u.numpy(), t_c.numpy(), 'o')
plt.show()
