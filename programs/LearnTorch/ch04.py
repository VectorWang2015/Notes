import numpy as np
import torch
import imageio

img_arr = imageio.imread('ch04.jpg')

# torch needs photos to be channelxHxW
img = torch.from_numpy(img_arr)
out = img.permute(2,0,1)
print(out.shape)

# create a batch, with NxCxHxW
batch_size = 100
batch = torch.zeros(batch_size, 3, 256, 256, dtype = torch.uint8)
print(batch.shape)
