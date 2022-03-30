import torch
import torch.optim as optim
from matplotlib import pyplot as plt


def model(t_u, w1, w2, b):
    return t_u**2 * w2 + t_u*w1 + b


def loss_fn(t_p, t_c):
    return ((t_p - t_c)**2).mean()


def train_loop(n_epochs, optimizer, params, train_t_u, val_t_u, train_t_c, val_t_c):
    for epoch in range(1, 1+n_epochs):
        train_t_p = model(train_t_u, *params)
        train_loss = loss_fn(train_t_p, train_t_c)

        optimizer.zero_grad()
        train_loss.backward()
        optimizer.step()

        if epoch <= 3 or epoch%200 == 0:
            with torch.no_grad():
                val_loss = loss_fn(model(val_t_u, *params), val_t_c)
                assert val_loss.requires_grad == False
            print("Epoch {}, Training loss {:.4f}, Validation loss {:.4f}".format(epoch, float(train_loss), float(val_loss)))

    return params



t_c = [0.5, 14.0, 15.0, 28.0, 11.0, 8.0, 3.0, -4.0, 6.0, 13.0, 21.0]
t_u = [35.7, 55.9, 58.2, 81.9, 56.3, 48.9, 33.9, 21.8, 48.4, 60.4, 68.4]
t_u = sorted(t_u)
t_c = sorted(t_c)

t_c = torch.tensor(t_c)
t_u = torch.tensor(t_u)

shuffle_i = torch.randperm(t_u.shape[0])
n_val = int(0.2 * t_u.shape[0])
train_i = shuffle_i[:-n_val]
val_i = shuffle_i[-n_val:]

train_t_u = t_u[train_i]
val_t_u = t_u[val_i]
train_t_c = t_c[train_i]
val_t_c = t_c[val_i]

train_t_un = train_t_u * 0.01
val_t_un = val_t_u * 0.01

params = torch.tensor([1.0, 1.0, 0.0], requires_grad=True)
learning_rate = 1e-2
optimizer = optim.SGD([params], lr=learning_rate)
params = train_loop(5000,
        optimizer,
        params,
        train_t_un,
        val_t_un,
        train_t_c,
        val_t_c)

t_p = model(t_u*0.01, *params)
fig = plt.figure(dpi=100)
plt.xlabel("Temperature (Fahrenheit)")
plt.ylabel("Temperature (Celsius)")
plt.plot(t_u.numpy(), t_p.detach().numpy())
plt.plot(t_u.numpy(), t_c.numpy(), 'o')
plt.show()
