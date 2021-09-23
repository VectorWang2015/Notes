import numpy as np
import ch1_funcs


a = np.arange(0,5,0.5)
print("a:")
print(a)

print("sigmoid a:")
print(ch1_funcs.sigmoid(a))

func_chain = [ch1_funcs.square, ch1_funcs.square]
print("deriv for func chain sq sq:")
print(ch1_funcs.chain_deriv_2(func_chain,a))

func_chain = [ch1_funcs.square, ch1_funcs.square, ch1_funcs.square]
print("deriv for func chain sq sq sq:")
print(ch1_funcs.chain_deriv_3(func_chain,a))


np.random.seed(20210923)
x = np.random.randn(3,3)
w = np.random.randn(3,2)

print("x:")
print(x)

print("w:")
print(w)

print("dl/dx:")
print(ch1_funcs.matrix_function_backward_sum_1(x,w,ch1_funcs.sigmoid))

print("gradient for 0,0")
x1 = x.copy()
x1[0,0] += 1e-3
result = (ch1_funcs.matrix_function_forward_sum(x1, w, ch1_funcs.sigmoid) - ch1_funcs.matrix_function_forward_sum(x, w, ch1_funcs.sigmoid)) / 1e-3
print(round(result, 4))
