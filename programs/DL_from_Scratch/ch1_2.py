import numpy as np


a = np.array([[1,2],[3,4]])
print("a: ")
print(a)

# sum(axis) can be seen as fold the matrix in the axis direction
# this line outputs [4,6]
print(a.sum(axis=0))
# this line outputs [3,7]
print(a.sum(axis=1))


# b is added to each line of a
# this can be convenient to add bias to a matrix
b = np.array([5,6])
print(a+b)
