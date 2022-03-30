import torch
import torchvision.transforms as tf
from PIL import Image
import os


"""
homework 1
"""
data_tf = tf.Compose([
    tf.Resize([200,200]),
    tf.ToTensor()
    ])

img_path = 'ch04-homework'
img_names = [name for name in os.listdir(img_path) if os.path.splitext(name)[-1] == '.jpg']

img_t = torch.zeros([len(img_names), 3, 200, 200], dtype=torch.float)
for i, image in enumerate(img_names):
    image = data_tf(Image.open(os.path.join(img_path, image)))
    img_t[i] = image

for i in range(img_t.shape[1]):
    print(torch.mean(img_t[:,i]))


"""
homework 2
"""
def clean_words(txt):
    punctuation = '!?,.;:"“”-_'
    words_list = txt.lower().split()
    words_list = [word.strip(punctuation) for word in words_list]
    return words_list


with open("gatsby.txt", 'r', encoding='ansi') as f:
    txt = f.read()
words_list = clean_words(txt)
words_set = sorted(set(words_list))
words2index = {}
for i, word in enumerate(words_set):
    words2index[word] = i

print(len(words2index))
#print(words2index)
words_t = torch.zeros([len(words_list), len(words_set)], dtype=torch.long)
print(words_t.shape)
for i, word in enumerate(words_list):
    words_t[i][words2index[word]] = 1

print(words_t.sum(dim=1).shape)
