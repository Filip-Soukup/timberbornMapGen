import random
import math
from matplotlib import pyplot as plt
import numpy as np

seed = 2023
size = (16, 16)
min = 4
max = 10
flatness = 4


def lerp(a, b, t):
    return round(a * (1 - t) + b * t)


def random_int(min: int, max: int, x: int, y: int, seed: int):
    random.seed(hash((seed, x, y)))
    num = random.random()
    return (round((max - min) * num) + min)


def noise_gen(seed, min, max, size, flatness):
    countX = math.ceil(size[0] / flatness)
    countY = math.ceil(size[1] / flatness)

    # list defining
    noise = [
        [0 for j in range(math.ceil(size[0] / flatness) * flatness + 1)]
        for i in range(math.ceil(size[1] / flatness) * flatness + 1)
    ]

    # main values
    for x in range(countX + 1):
        for y in range(countY + 1):
            noise[x * flatness][y * flatness] = random_int(min, max, x, y, seed)

    # grid values
    for x in range(countX + 1):
        for y in range(math.ceil(size[1] / flatness) * flatness + 1):
            if y % flatness != 0:
                noise[x * flatness][y] = lerp(noise[x * flatness][(y // flatness) * flatness],
                                              noise[x * flatness][(y // flatness + 1) * flatness],
                                              (y % flatness) / flatness)

    for x in range(math.ceil(size[0] / flatness) * flatness + 1):
        for y in range(math.ceil(size[1] / flatness) * flatness + 1):
            if x % flatness != 0:
                noise[x][y] = lerp(noise[(x // flatness) * flatness][y], noise[(x // flatness + 1) * flatness][y],
                                   (x % flatness) / flatness)

    # map = slice(noise)

    return noise


def visualize_heightmap(heightmap):
    heightmap_np = np.array(heightmap)
    plt.imshow(heightmap_np, cmap='gray', interpolation='nearest')
    plt.colorbar()
    plt.show()


heightmap = noise_gen(seed, min, max, size, flatness)

for k in heightmap:
    print(k)
visualize_heightmap(heightmap)