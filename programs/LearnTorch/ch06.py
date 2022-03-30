import torch
import torch.optim as optim
import torch.nn as nn
from matplotlib import pyplot as plt
from collections import OrderedDict
from matplotlib import pyplot as plt


def model(t_u, w, b):
    return w*t_u + b


# MSE mean square err
def loss_fn(t_p, t_c):
    squared_diffs = (t_p - t_c) ** 2
    return squared_diffs.mean()


def training_loop(n_epochs, optimizer, model, loss_fn,
        t_u_train, t_u_val, t_c_train, t_c_val):
    for epoch in range(1, n_epochs+1):
        t_p_train = model(t_u_train)
        loss_train = loss_fn(t_p_train, t_c_train)
        with torch.no_grad():
            t_p_val = model(t_u_val)
            loss_val = loss_fn(t_p_val, t_c_val)
        # set grad to 0, backward, update params
        optimizer.zero_grad()
        loss_train.backward()
        optimizer.step()
        if epoch == 1 or epoch%500 == 0:
            print("Epoch {}, Training loss {:.4f}, Val loss {:.4f}".format(
                epoch, loss_train.item(), loss_val.item()))


t_c = [0.5, 14.0, 15.0, 28.0, 11.0, 8.0, 3.0, -4.0, 6.0, 13.0, 21.0]
t_u = [35.7, 55.9, 58.2, 81.9, 56.3, 48.9, 33.9, 21.8, 48.4, 60.4, 68.4]

t_c = torch.tensor(t_c).unsqueeze(1)
t_u = torch.tensor(t_u).unsqueeze(1)
device = torch.device("cuda:0")

# take 80% as train set
n_samples = t_u.shape[0]
n_val = int(0.2 * n_samples)
shuffled_indices = torch.randperm(n_samples)
train_indices = shuffled_indices[:-n_val]
val_indices = shuffled_indices[-n_val:]
#print(train_indices, val_indices)

train_t_u = t_u[train_indices]
train_t_c = t_c[train_indices]
val_t_u = t_u[val_indices]
val_t_c = t_c[val_indices]

train_t_un = 0.1 * train_t_u
val_t_un = 0.1 * val_t_u

#print(val_t_un)

"""
# params: input feature num, output feature num, enable bias = True
linear_model = nn.Linear(1, 1)

optimizer = optim.SGD(linear_model.parameters(),
        lr=1e-2
        )

training_loop(3000,
    optimizer,
    linear_model,
    nn.MSELoss(),
    train_t_un,
    val_t_un,
    train_t_c,
    val_t_c
    )
#print(linear_model.weight)
#print(linear_model.bias)
#print(linear_model.parameters())
"""

"""
seq_model = nn.Sequential(nn.Linear(1,13),
        nn.Tanh(),
        nn.Linear(13,1))
print(seq_model)
# output should be: first linear's weights, first linear's bias
# second linear's weights, second linear's bias
print([param.shape for param in seq_model.parameters()])

for name, param in seq_model.named_parameters():
    print(name, param.shape)
"""

seq_model = nn.Sequential(OrderedDict([
    ('hidden_linear', nn.Linear(1,13)),
    ('hidden_activation', nn.Tanh()),
    ('output_linear', nn.Linear(13,1))
    ]))
print(seq_model)
for name, param in seq_model.named_parameters():
    print(name, param.shape)
print(seq_model.output_linear.bias)

optimizer = optim.SGD(seq_model.parameters(), lr=1e-3)
training_loop(50000,
    optimizer,
    seq_model,
    nn.MSELoss(),
    train_t_un,
    val_t_un,
    train_t_c,
    val_t_c
    )

print('output', seq_model(val_t_un))
print('answer', val_t_c)
print('hidden', seq_model.hidden_linear.weight.grad)

t_range = torch.arange(20.,90.).unsqueeze(1)
fig = plt.figure(dpi=200)
plt.xlabel("Fahrenheit")
plt.ylabel("Celsius")
plt.plot(t_u.numpy(), t_c.numpy(), 'o')
plt.plot(t_range.numpy(), seq_model(0.1*t_range).detach().numpy(), 'c-')
plt.plot(t_u.numpy(), seq_model(0.1*t_u).detach().numpy(), 'kx')
plt.show()
