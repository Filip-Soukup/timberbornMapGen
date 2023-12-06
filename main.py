import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import zipfile
import os
from opensimplex import OpenSimplex
import copy


def find_closest_flat_space(heightmap):
    def is_flat_space(i, j):
        center_value = heightmap[i][j]
        for x in range(i - 1, i + 2):
            for y in range(j - 1, j + 2):
                if heightmap[x][y] != center_value:
                    return False
        return True

    rows, cols = len(heightmap), len(heightmap[0])
    min_distance = float('inf')
    result_coords = None

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if is_flat_space(i, j):
                # Calculate distance to the center
                distance = abs(i - (rows // 2)) + abs(j - (cols // 2))

                # Update result if closer
                if distance < min_distance:
                    min_distance = distance
                    result_coords = (i, j)

    return result_coords


def visualize_heightmap(heightmap):
    heightmap_np = np.array(heightmap)
    plt.imshow(heightmap_np, cmap='gray', interpolation='nearest')
    plt.colorbar()
    plt.show()


matplotlib.use('TkAgg')

map_gen_name = "PYmberGen"

seed = 42
size = (128, 128)
minimum = 2
maximum = 14
flatness = 64

noise_generator = OpenSimplex(seed)
heightmap = [
    [
        round(((noise_generator.noise2(x/flatness, y/flatness) + 1)/2) * (maximum - minimum) + minimum)
        for y in range(size[1]-1)
    ]
    for x in range(size[0]-1)
]

# print(heightmap)

start_loc = find_closest_flat_space(heightmap)
print(start_loc)

visualize_heightmap(heightmap)

fluid_heightmap = " ".join(["0"] * (size[0] * size[1]))
fluid_direction_map = " ".join(["0:0:0:0"] * (size[0] * size[1]))

world_json = (f'''{{
  "GameVersion":"0.5.3.2-3a67edf-xsw",
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