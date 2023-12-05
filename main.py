import random
import math
from matplotlib import pyplot as plt
import numpy as np
import zipfile
import os

map_gen_name = "insert name later lol"

seed = 2023
size = (256, 256)
minimum = 0
maximum = 10
flatness = 32


def lerp(a, b, t):
    return a * (1 - t) + b * t


def random_int(min: int, max: int, x: int, y: int, seed: int):
    random.seed(hash((seed, x, y)))
    num = random.random()
    return round((max - min) * num + min)


def noise_gen(seed, min, max, size, flatness):
    count_x = math.ceil(size[0] / flatness)
    count_y = math.ceil(size[1] / flatness)

    # list defining
    noise = [
        [0 for j in range(math.ceil(size[0] / flatness) * flatness + 1)]
        for i in range(math.ceil(size[1] / flatness) * flatness + 1)
    ]

    # main values
    for x in range(count_x + 1):
        for y in range(count_y + 1):
            noise[x * flatness][y * flatness] = random_int(min, max, x, y, seed)

    # grid values
    for x in range(count_x + 1):
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


heightmap = noise_gen(seed, minimum, maximum, size, flatness)
heightmap = [[round(element) for element in row[0:size[1]]] for row in heightmap[0:size[0]]]

# print(heightmap)

visualize_heightmap(heightmap)

fluid_heightmap = " ".join(["0"] * (size[0] * size[1]))
fluid_direction_map = " ".join(["0:0:0:0"] * (size[0] * size[1]))

world_json = (f'''{{
  "GameVersion":"0.5.3.2-3a67edf-xsw",
  "MadeWith": "{map_gen_name}",
  "Timestamp":"INSERT CREATION TIME",
  "Singletons":{{
    "MapSize":{{
      "Size":{{
        "X":{size[0]},
        "Y":{size[1]}
      }}
    }},
    "TerrainMap":{{
      "Heights":{{
        "Array":"{' '.join(' '.join(map(str, sublist)) for sublist in heightmap)}"
      }}
    }},
    "CameraStateRestorer":{{
      "SavedCameraState":{{
        "Target":{{
          "X":0.0,
          "Y":0.0,
          "Z":0.0
        }},
        "ZoomLevel":0.0,
        "HorizontalAngle":30.0,
        "VerticalAngle":70.0
      }}
    }},
    "WaterMap":{{
      "WaterDepths":{{
        "Array":"{fluid_heightmap}"
      }},
      "Outflows":{{
        "Array":"{fluid_direction_map}"
      }}
    }},
    "ContaminationMap":{{
      "Contaminations":{{
        "Array":"{fluid_heightmap}"
      }}
    }},
    "HazardousWeatherHistory":{{
      "History":[]
    }},
    "MapThumbnailCameraMover":{{
      "CurrentConfiguration":{{
        "Position":{{
          "X":128.0,
          "Y":164.553619,
          "Z":-68.10739
        }},
        "Rotation":{{
          "X":0.342020124,
          "Y":0.0,
          "Z":0.0,
          "W":0.9396926
        }},
        "ShadowDistance":150.0
      }}
    }}
  }},
  "Entities":[]
}}''')

map_metadata_json = f'''{{
    "Width":{size[0]},
    "Height":{size[1]},
    "MapNameLocKey":"",
    "MapDescriptionLocKey":"",
    "MapDescription":"Generated using {map_gen_name}",
    "IsRecommended":false,
    "IsDev":false
}}'''

with open("template/map_metadata.json", "w") as map_metadata_file:
    map_metadata_file.write(map_metadata_json)
with open("template/world.json", "w") as world_file:
    world_file.write(world_json)

with zipfile.ZipFile('GeneratedMap.timber', 'w') as timber_file:
    for root, _, files in os.walk("template"):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, "template")
            timber_file.write(file_path, arcname)