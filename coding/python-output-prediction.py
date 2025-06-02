# Prompt:
# What is the output of this Python code?
# 
# ```
# { program }
# ```
# 
# Give only the exact output from this code, no commentary.
# If the code produces an exception, provide the error.

data = [1, 2, 3]
for i, x in enumerate(data):
    print(x + i, end=' ')
# 1 3 5 

data = [1,]
data.pop()
if data: print('Got data')
# (no output)

import numpy as np
arr = np.arange(9).reshape(3,3)
print(arr[:, 1])
# [1, 4, 7]

def sqrt(n): return n**0.5
print(sqrt(-9) == -9**0.5)
# False

print(1 > 0 < 1)
# True

if 0.1 + 0.2 == 0.3: print('Yup')
# (no output)

class Geo:
    pass
print(Geo() == Geo())
# False

d = {}
d[5.0] = 'five-oh'
d[5] = 'five'
print(d)
# {5.0: 'five'}

print(~True)
# -2

print({'a': 1, 'b': 2} == {'b': 2, 'a': 1})
# True

print('obiwan'.count(''))
# 7

print(True == False is False)
# False

() = ()
# (no output)

t = [1],
t[0] += [2]
# TypeError: 'tuple' object does not support item assignment

def j(i): return i * 1j
print(complex(j(j(1)), j(j(-1))))
# (-1+1j)

foos = foos = [lambda:f"Function {i}" for i in range(3)]
print(foos[0]())
# Function 2
