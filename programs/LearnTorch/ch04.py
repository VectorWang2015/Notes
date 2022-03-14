import numpy as np
import torch
import os
import csv
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

data_dir = "p1ch4/image-cats"
filenames = [ name for name in os.listdir(data_dir) if os.path.splitext(name)[-1] == '.png']
print(len(filenames))

for i, name in enumerate(filenames):
    img_arr = imageio.imread(os.path.join(data_dir, name))
    img_t = torch.from_numpy(img_arr)
    img_t = img_t.permute(2,0,1)
    # remove transparency layer if any
    img_t = img_t[:3]

    batch[i] = img_t

#print(batch.shape)
#print(batch.dtype)

batch = batch.float()
"""
batch /= 255
print(batch.dtype)
"""

n_channels = batch.shape[1]
for c in range(n_channels):
    # mean is a 0-axis tensor
    mean = torch.mean(batch[:,c])
    # std is a 0-axis tensor
    std = torch.std(batch[:,c])
    batch[:,c] = (batch[:,c] - mean) / std
#print(batch)


dir_path = "p1ch4/volumetric-dicom/2-LUNG 3.0  B70f-04083/"
vol_arr = imageio.volread(dir_path, 'DICOM')
print(vol_arr.shape)
vol = torch.from_numpy(vol_arr).float()
vol = torch.unsqueeze(vol,1) # insert a channel axis at 1, with dimension 1
vol = torch.unsqueeze(vol,2) # insert a depth axis at 2, with dimension 1
print(vol.shape)


wine_path = "p1ch4/tabular-wine/winequality-white.csv"
wineq_numpy = np.loadtxt(wine_path, dtype=np.float32, delimiter=";", skiprows=1)
print(wineq_numpy)

# take first row to show titles
col_list = next(csv.reader(open(wine_path), delimiter=';'))
print(wineq_numpy.shape)
print(col_list)

wineq = torch.from_numpy(wineq_numpy)
print(wineq.shape, wineq.dtype)

# take out last col as labels
wine_data = wineq[:,:-1]
print(wine_data.shape)
# take last col 'quality' as labels
target = wineq[:, -1]
print(target, target.shape)

# need to convert to int first
target = target.long()
# second way to handle labels, one hot
target_onehot = torch.zeros(target.shape[0], 10)
print(target_onehot, target_onehot.dtype)
# axis to apply one-hot, src tensor, the value to be set
a = target_onehot.scatter_(1, target.unsqueeze(1), 1.0)
print(a, a.shape)

data_mean = torch.mean(wine_data, dim=0)
print(data_mean)
data_var = torch.var(wine_data, dim=0)
print(data_var)

data_normalized = (wine_data - data_mean) / torch.sqrt(data_var)
#data_normalized1 = (wine_data - data_mean) / torch.std(wine_data, dim=0)
print(data_normalized)
#print(data_normalized1)

bad_index = target <= 3
bad_data = wine_data[bad_index]
print(bad_data, bad_data.shape)
mid_data = wine_data[(target>3) & (target<7)]
good_data = wine_data[target >= 7]

bad_mean = torch.mean(bad_data, dim=0)
mid_mean = torch.mean(mid_data, dim=0)
good_mean = torch.mean(good_data, dim=0)

for i, args in enumerate(zip(col_list, bad_mean, mid_mean, good_mean)):
    print('{:2} {:20} {:6.2f} {:6.2f} {:6.2f}'.format(i, *args))


total_sulfur_threshold = 141.83
total_sulfur_data = wine_data[:,6]
# lt can select index in A which have less value than B
predicted_index = torch.lt(total_sulfur_data, total_sulfur_threshold)
#predicted_index2 = total_sulfur_data < total_sulfur_threshold

print(predicted_index.sum())
#print(predicted_index2.sum())

actual_index = target > 5
n_matches = torch.sum(actual_index & predicted_index).item()
print(n_matches)
