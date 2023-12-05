import random

seed = 2023
x, y = 5, 5

random.seed(hash((seed, x, y)))
print(random.random())
random.seed(hash((seed, x-y, y-x)))
print(random.random())
