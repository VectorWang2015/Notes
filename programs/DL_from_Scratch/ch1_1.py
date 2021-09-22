import numpy as np


print("Python list operations:")

a = [1,2,3]
b = [4,5,6]

print("a+b: {}".format(a+b))

try:
    print(a*b)
except:
    print("a*b has no meaning for python lists")

print()
print("numpy array operations:")

a = np.array([1,2,3])
b = np.array([4,5,6])

print("a+b: {}".format(a+b))
print("a*b: {}".format(a*b))
