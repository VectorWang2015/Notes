import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
import datetime
from collections import OrderedDict
from torchvision import datasets, transforms
from matplotlib import pyplot as plt


device = (torch.device('cuda') if torch.cuda.is_available()
        else torch.device('cpu'))
data_path = './data_unversioned/p1ch7'
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

label_map = {0:0, 2:1}
class_names = ['airplane', 'bird']
cifar2 = [(img, label_map[label]) for img, label in cifar10 if label in [0,2]]
cifar2_val = [(img, label_map[label]) for img, label in cifar10_val if label in [0,2]]

"""
# in_ch, out_ch, kernel size (3,3)
conv = nn.Conv2d(3, 16, kernel_size=3, padding=1)
pool = nn.MaxPool2d(2)
print(conv)
print(conv.weight.shape, conv.bias.shape)

img, _ = cifar2[0]
#output = conv(img.unsqueeze(0))
output = pool(img.unsqueeze(0))

print(img.unsqueeze(0).shape, output.shape)

ax1 = plt.subplot(1,2,1)
plt.title('output')
plt.imshow(output[0,0].detach(), cmap='gray')
plt.subplot(1,2,2, sharex=ax1, sharey=ax1)
plt.imshow(img.mean(0), cmap='gray')
plt.title('input')
plt.show()
"""

#img, _ = cifar2[0]

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 8, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(8*8*8, 32)
        self.fc2 = nn.Linear(32,2)

    def forward(self, x):
        out = F.max_pool2d(torch.tanh(self.conv1(x)), 2)
        out = F.max_pool2d(torch.tanh(self.conv2(out)), 2)

        out = out.view(-1, 8*8*8)
        out = torch.tanh(self.fc1(out))
        out = self.fc2(out)
        return out


class NetDropout(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 8, kernel_size=3, padding=1)
        # p is the percentage to be dropped
        self.conv1_dropout = nn.Dropout2d(p=0.4)
        self.conv2_dropout = nn.Dropout2d(p=0.4)
        self.fc1 = nn.Linear(8*8*8, 32)
        self.fc2 = nn.Linear(32,2)

    def forward(self, x):
        out = F.max_pool2d(torch.tanh(self.conv1(x)), 2)
        out = self.conv1_dropout(out)
        out = F.max_pool2d(torch.tanh(self.conv2(out)), 2)
        out = self.conv2_dropout(out)

        out = out.view(-1, 8*8*8)
        out = torch.tanh(self.fc1(out))
        out = self.fc2(out)
        return out


class NetBatchNorm(nn.Module):
    def __init__(self, n_chs1=32):
        super().__init__()
        self.n_chs1 = n_chs1
        self.conv1 = nn.Conv2d(3, self.n_chs1, kernel_size=3, padding=1)
        self.conv1_batchnorm = nn.BatchNorm2d(num_features=n_chs1)
        self.conv2 = nn.Conv2d(self.n_chs1, self.n_chs1//2, kernel_size=3, padding=1)
        self.conv2_batchnorm = nn.BatchNorm2d(num_features=n_chs1//2)
        # p is the percentage to be dropped
        self.fc1 = nn.Linear(8*8*self.n_chs1//2, 32)
        self.fc2 = nn.Linear(32,2)

    def forward(self, x):
        out = self.conv1_batchnorm(self.conv1(x))
        out = F.max_pool2d(torch.tanh(out), 2)

        out = self.conv2_batchnorm(self.conv2(out))
        out = F.max_pool2d(torch.tanh(out), 2)

        out = out.view(-1, 8*8*self.n_chs1//2)
        out = torch.tanh(self.fc1(out))
        out = self.fc2(out)
        return out


class NetRes(nn.Module):
    def __init__(self, n_chs1=32):
        super().__init__()
        self.n_chs1 = n_chs1
        self.conv1 = nn.Conv2d(3, self.n_chs1, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(self.n_chs1, self.n_chs1//2, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(self.n_chs1//2, self.n_chs1//2, kernel_size=3, padding=1)

        self.fc1 = nn.Linear(4*4*self.n_chs1//2, 32)
        self.fc2 = nn.Linear(32, 2)

    def forward(self, x):
        out = F.max_pool2d(torch.relu(self.conv1(x)), 2)
        out = F.max_pool2d(torch.relu(self.conv2(out)), 2)
        out1 = out
        
        out = torch.relu(self.conv3(out))
        out = F.max_pool2d(out + out1, 2)

        out = out.view(-1, 4*4*self.n_chs1//2)
        out = torch.relu(self.fc1(out))
        out = self.fc2(out)

        return out


class ResBlock(nn.Module):
    def __init__(self, n_chs):
        super(ResBlock, self).__init__()
        # bias is not needed as using batch norm
        self.conv = nn.Conv2d(n_chs, n_chs, kernel_size=3,
                padding=1, bias=False)
        self.batch_norm = nn.BatchNorm2d(num_features=n_chs)

        nn.init.kaiming_normal_(self.conv.weight,
                nonlinearity='relu')
        nn.init.constant_(self.batch_norm.weight, 0.5)
        nn.init.zeros_(self.batch_norm.bias)

    def forward(self, x):
        out = self.conv(x)
        out = self.batch_norm(out)
        out = torch.relu(out)
        return out+x


class NetResDeep(nn.Module):
    def __init__(self, n_chs=32, n_blocks=10):
        super().__init__()
        self.n_chs = n_chs
        self.conv1 = nn.Conv2d(3, self.n_chs, kernel_size=3, padding=1)
        # are these resblocks different?
        """
        self.resblocks = nn.Sequential(
                *(n_blocks * [ResBlock(n_chs=self.n_chs)]))
        """
        """
        res_lst = n_blocks * [ResBlock(n_chs=n_chs)]
        print(res_lst[0] is res_lst[1]) # result True
        self.resblocks = nn.Sequential(*res_lst)
        """
        # a more solid way?
        res_lst = []
        for i in range(n_blocks):
            res_lst.append(ResBlock(n_chs=n_chs))
        #print(res_lst[0] is res_lst[1])
        self.resblocks = nn.Sequential(*res_lst)

        self.fc1 = nn.Linear(8*8*self.n_chs, 32)
        self.fc2 = nn.Linear(32, 2)

    def forward(self, x):
        out = F.max_pool2d(torch.relu(self.conv1(x)), 2)
        out = self.resblocks(out)
        out = F.max_pool2d(out, 2)
        out = out.view(-1, 8*8*self.n_chs)
        out = torch.relu(self.fc1(out))
        out = self.fc2(out)

        return out

def training_loop(n_epochs, optimizer, model, loss_fn, train_loader):
    model.train()
    for epoch in range(1, n_epochs + 1):
        loss_train = 0.0
        for imgs, labels in train_loader:
            imgs = imgs.to(device)
            labels = labels.to(device)
            outputs = model(imgs)
            loss = loss_fn(outputs, labels)

            # L2
            l2_lambda = 0.001
            p_pow = sum(p.pow(2.0).sum() for p in model.parameters())
            loss += p_pow * l2_lambda

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            loss_train += loss.item()

        if epoch == 1 or epoch % 10 == 0:
            print('{} Epoch {}, Training loss {}'.format(
                datetime.datetime.now(), epoch, loss_train/len(train_loader)
            ))

def validate(model, train_loader, val_loader):
    model.eval()
    for name, loader in [("train", train_loader), ("val", val_loader)]:
        correct = 0
        total = 0
        with torch.no_grad():
            for imgs, labels in loader:
                imgs = imgs.to(device)
                labels = labels.to(device)
                outputs = model(imgs)
                _, predicted = torch.max(outputs, dim=1)
                total += labels.shape[0]
                correct += int((predicted==labels).sum())

        print("Accuracy {}: {:.2f}".format(name, correct/total))


if __name__ == "__main__":
    print("Training on device {}.".format(device))
    model = NetResDeep().to(device)
    #numel_list = [p.numel() for p in model.parameters()]
    #print(sum(numel_list), numel_list)
    #print(model(img.unsqueeze(0)))
    train_loader = torch.utils.data.DataLoader(cifar2, batch_size=64, shuffle=True)
    val_loader = torch.utils.data.DataLoader(cifar2_val, batch_size=64, shuffle=True)
    optimizer = torch.optim.SGD(model.parameters(), lr=1e-2)
    loss_fn = nn.CrossEntropyLoss()
    
    training_loop(n_epochs=100,
            optimizer=optimizer,
            model=model,
            loss_fn=loss_fn,
            train_loader=train_loader
            )
    validate(model=model,
            train_loader=train_loader,
            val_loader=val_loader
            )
    
    torch.save(model.state_dict(), './birds_vs_airplanes.pt')
    #model.load_state_dict(torch.load('./birds_vs_airplanes.pt'))
