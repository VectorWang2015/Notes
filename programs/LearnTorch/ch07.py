import torch
import ssl
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from matplotlib import pyplot as plt

ssl._create_default_https_context = ssl._create_unverified_context

data_path = './data_unversioned/p1ch7'
"""
# download train set
cifar10 = datasets.CIFAR10(data_path, train=True, download=True, transform=transforms.ToTensor())
# download validation set
cifar10_val = datasets.CIFAR10(data_path, train=False, download=True, transform=transforms.ToTensor())

# torch.utils.data.dataset.Dataset
# it contains two methods: __len__, __getitem__
#print(type(cifar10).__mro__)

#print(len(cifar10))
#print(len(cifar10_val))

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
        'dog', 'frog', 'horse', 'ship', 'truck']

# img is a tensor
img_t, label = cifar10[99]
#print(img_t.shape, img_t.dtype, label, class_names[label])
#print(img_t.min(), img_t.max())

# to change axis from cxhxw -> hxwxc
#plt.imshow(img_t.permute(1,2,0))
#plt.show()

# stack all imgs to dim3
imgs = torch.stack([img_t for img_t, _ in cifar10], dim=3)
print(imgs.shape)   # 3,32,32,50000

img_mean = imgs.view(3,-1).mean(dim=1)
img_std = imgs.view(3,-1).std(dim=1)
print(img_mean) # 0.4914, 0.4822, 0.4465
print(img_std)  # 0.2470, 0.2435, 0.2616
"""
# download train set
cifar10 = datasets.CIFAR10(data_path, train=True, download=True,
        transform=transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465),
                                (0.2470, 0.2435, 0.2616)),
            #transforms.RandomCrop(26)
            ]))
# download validation set
cifar10_val = datasets.CIFAR10(data_path, train=False, download=True,
        transform=transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465),
                                (0.2470, 0.2435, 0.2616)),
            #transforms.RandomCrop(26)
            ]))

#img_t, _ = cifar10[99]
#plt.imshow(img_t.permute(1,2,0))
#plt.show()

device = torch.device("cuda:0")
label_map = {0:0, 2:1}
class_names = ['airplane', 'bird']
cifar2 = [(img, label_map[label]) for img, label in cifar10 if label in [0,2]]
cifar2_val = [(img, label_map[label]) for img, label in cifar10_val if label in [0,2]]

n_out = 2

model =nn.Sequential(
    nn.Linear(32*32*3, 64),
    nn.Tanh(),
    #nn.Linear(1024, 512),
    #nn.Tanh(),
    #nn.Linear(512, 128),
    #nn.Tanh(),
    nn.Linear(64, n_out),
    ).to(device)

#img, label = cifar2[0]
#img_batch = img.view(-1).unsqueeze(0)

loss_fn = nn.CrossEntropyLoss()
#loss_fn = nn.MSELoss()

learning_rate = 1e-2
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
n_epochs = 100
for epoch in range(1, n_epochs+1):
    train_loader = torch.utils.data.DataLoader(cifar2, batch_size=64, shuffle=True)
    for imgs, labels in train_loader:
        imgs = imgs.to(device)
        labels = labels.to(device)
        #labels_onehot = torch.zeros(labels.shape[0], 2).to(device)
        #for i in range(labels.shape[0]):
            #labels_onehot[i][labels[i]] = 1
        batch_size = imgs.shape[0]
        outputs = model(imgs.view(batch_size, -1))
        loss = loss_fn(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print("Epoch {}, Loss {:.4f}".format(epoch, loss))


val_loader = torch.utils.data.DataLoader(cifar2_val, batch_size=64, shuffle=True)
correct = 0
total = 0
with torch.no_grad():
    for imgs, labels in val_loader:
        imgs = imgs.to(device)
        labels = labels.to(device)
        batch_size = imgs.shape[0]
        outputs = model(imgs.view(batch_size, -1))
        _, predicted = outputs.max(dim=1)
        total+=batch_size
        correct+=int((predicted==labels).sum())
print("Accuracy: {:.4f}".format(correct/total))

numel_list = [p.numel()
        for p in model.parameters()
        if p.requires_grad == True]
print(sum(numel_list), numel_list)
