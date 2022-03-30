import ch08
import torch
from torchvision import datasets, transforms, utils
import numpy as np
import os.path
from matplotlib import pyplot as plt
import random
from PIL import Image



model = ch08.NetResDeep()
model.load_state_dict(torch.load('./birds_vs_airplanes.pt'))

npy_bird_path = './i95_bird.npy'
npy_plane_path = './i95_plane.npy'

def select(cifar10):
    model.eval()
    p_index = []
    b_index = []
    for i, pair in enumerate(cifar10):
        img, label = pair
        # skip bird or plane pics
        if i==0 or (i+1) % 1000 == 0:
            print("Finished loop: ", i+1)

        if label == 0 or label == 2:
            continue
        
        img = img.unsqueeze(0)
        result = torch.softmax(model(img), dim=1)
        max_values, max_index = result.max(dim=1)
        if max_values.item() > 0.95:
            if max_index.item() == 0:
                p_index.append(i)
            elif max_index.item() == 1:
                b_index.append(i)

    return p_index, b_index

def bird_like_selector(cifar10):
    while True:
        ri = random.randint(0, len(i_95_b)-1)
        sample_bird_img = cifar10[i_95_b[ri]][0]
        sample_bird_label = cifar10[i_95_b[ri]][1]
        #np.save('./data_unversioned/like_bird.npy', sample_bird_img.numpy())
        plt.imshow(sample_bird_img.permute(1,2,0))
        utils.save_image(sample_bird_img, './data_unversioned/like_bird.png')
        plt.show()

def extinguish_img(img_path):
    model.eval()
    img = Image.open(img_path)

    # remove transparency
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    trans_fn = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465),
            (0.2470, 0.2435, 0.2616)),
        ])
    img = trans_fn(img).unsqueeze(0)
    result = model(img)
    _, index = result.max(dim=1)

    if index.item() == 0:
        print(img_path, " is plane")
    if index.item() == 1:
        print(img_path, " is bird")

def rand_plane(img_path):
    cifar2 = [img for img, label in cifar10
            if label==0]
    randindex = random.randint(0, len(cifar2)-1)
    img =  cifar2[randindex]
    #trans_fn = transforms.Compose([transforms.ToTensor()])
    #img = trans_fn(img)

    utils.save_image(img, img_path)
    return img



if __name__ == "__main__":
    if not (os.path.exists(npy_plane_path) and
            os.path.exists(npy_bird_path)):
        print("Selecting required imgs")
        cifar10_norm = ch08.cifar10
        #cifar10_val_norm = ch08.cifar10_val
        i_95_p, i_95_b = select(cifar10_norm)
        i_95_p = np.array(i_95_p)
        i_95_b = np.array(i_95_b)
        np.save(npy_plane_path, i_95_p)
        np.save(npy_bird_path, i_95_b)
    else:
        print("Save file found")
        i_95_p = np.load(npy_plane_path)
        i_95_b = np.load(npy_bird_path)
    data_path = './data_unversioned/p1ch7'
    # download train set
    cifar10 = datasets.CIFAR10(data_path, train=True, download=True,
            transform=transforms.Compose([
                transforms.ToTensor(),
                #transforms.RandomCrop(26)
                ]))

    print(len(i_95_p))
    print(len(i_95_b))

    #bird_like_selector(cifar10)
    #extinguish_img('./data_unversioned/like_bird_changed.png')

    #img = rand_plane('./data_unversioned/plane.png')
    extinguish_img('./data_unversioned/plane_like_bird.png')
