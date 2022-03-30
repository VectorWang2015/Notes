import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from matplotlib import pyplot as plt
from collections import OrderedDict


device = torch.device('cuda:0')

def calculate_accuracy(t_1, t_ans):
    t_1 = t_1.max(dim=1)[1] # need index only
    t_ans = t_ans.max(dim=1)[1]
    t_acc = (t_1 <= t_ans+1) & (t_1 >= t_ans-1)
    return float(t_acc.sum() / t_acc.shape[0])


def training_loop(n_epochs,
        model,
        optimizer,
        loss_fn,
        acc_fn,
        t_train_u,
        t_train_c,
        t_val_u,
        t_val_c):
    for epoch in range(1, n_epochs+1):
        t_train_p = model(t_train_u)
        t_train_loss = loss_fn(t_train_p, t_train_c)
        # train
        optimizer.zero_grad()
        t_train_loss.backward()
        optimizer.step()

        if epoch <= 5 or epoch%100 == 0:
            with torch.no_grad():
                t_val_p = model(t_val_u)
                t_val_loss = loss_fn(t_val_p, t_val_c)
                n_val_acc = acc_fn(t_val_p, t_val_c)
                print("Epoch: {}, val loss: {:.4f}, val acc: {:.4f}".format(epoch, t_val_loss, n_val_acc))


# read data from csv
wine_path = "p1ch4/tabular-wine/winequality-white.csv"
wine_raw_numpy = np.loadtxt(wine_path, dtype=np.float32, delimiter=';', skiprows=1)
#print(wine_raw_numpy.shape)
#print(wine_raw_numpy)

# seperate wine properties and quality
t_wine_property = torch.from_numpy(wine_raw_numpy)[:,:-1]
# convert to long, as scatter_ needs long to work
t_wine_quality = torch.from_numpy(wine_raw_numpy)[:,-1:].long() - 1
#print(t_wine_property.shape)
#print(t_wine_quality.shape)

# one-hot encode quality as result
t_wine_quality_onehot = torch.zeros(t_wine_quality.shape[0], 10)
t_wine_quality_onehot.scatter_(1, t_wine_quality, 1.0)

# normalize
t_wine_property_mean = t_wine_property.mean(dim=0)
t_wine_property_std = t_wine_property.std(dim=0)
t_wine_property = (t_wine_property - t_wine_property_mean) / t_wine_property_std

# permute and seperate train & validation set
n_val = int(0.2 * t_wine_quality.shape[0])
t_indices = torch.randperm(t_wine_quality.shape[0])
t_train_indices = t_indices[:-n_val]
t_val_indices = t_indices[-n_val:]

t_train_p = t_wine_property[t_train_indices].to(device)
t_train_q = t_wine_quality_onehot[t_train_indices].to(device)
t_val_p = t_wine_property[t_val_indices].to(device)
t_val_q = t_wine_quality_onehot[t_val_indices].to(device)
#print(t_train_p.shape, t_train_q.shape, t_val_p.shape, t_val_q.shape)

# network and train
learning_rate = 1e-2
seq_model = nn.Sequential(OrderedDict([
    ('hidden_linear', nn.Linear(11, 96)),
    ('hidden_activation', nn.ReLU()),
    ('hidden_linear2', nn.Linear(96, 96)),
    ('hidden_activation2', nn.ReLU()),
    ('hidden_linear3', nn.Linear(96, 96)),
    ('hidden_activation3', nn.ReLU()),
    ('output_linear', nn.Linear(96, 10)),
    ('output_activation', nn.Softmax())
    ])).to(device)
#for name, param in seq_model.named_parameters():
    #print(name, param)
optimizer = optim.SGD(seq_model.parameters(), lr=learning_rate)

# training and conclusion
training_loop(5000,
        seq_model,
        optimizer,
        nn.MSELoss(),
        calculate_accuracy,
        t_train_p,
        t_train_q,
        t_val_p,
        t_val_q)
