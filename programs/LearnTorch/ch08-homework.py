import ch08
import torch
import numpy as np
import os.path
from matplotlib import pyplot as plt


cifar10 = ch08.cifar10
cifar10_val = ch08.cifar10_val

model = ch08.NetResDeep()
model.load_state_dict(torch.load('./birds_vs_airplanes.pt'))

npy_path = './i95.npy'

def select():
    model.eval()
    index = []
    for i, pair in enumerate(cifar10):
        img, label = pair
        # skip bird or plane pics
        if i==0 or (i+1) % 1000 == 0:
            print("Finished loop: ", i+1)

        if label == 0 or label == 2:
            continue
        
        img = img.unsqueeze(0)
        result = torch.softmax(model(img), dim=1)
        max_values, _ = result.max(dim=1)
        if max_values.item() > 0.95:
            index.append(i)

    return index


if __name__ == "__main__":
    if not os.path.exists(npy_path):
        print("Selecting required imgs")
        i_95 = select()
        i_95 = np.array(i_95)
        np.save(npy_path, i_95)
    else:
        print("Save file found")
        i_95 = np.load(npy_path)

    print(len(i_95))
