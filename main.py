import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import zipfile
import os
from opensimplex import OpenSimplex


def visualize_heightmap(heightmap):
    heightmap_np = np.array(heightmap)
    plt.imshow(heightmap_np, cmap='gray', interpolation='nearest')
    plt.colorbar()
    plt.show()


matplotlib.use('TkAgg')

map_gen_name = "insert name later lol"

seed = 69
size = (69, 69)
minimum = 4
maximum = 16
flatness = 32

noise_generator = OpenSimplex(seed=42)
heightmap = [
    [
        round(((noise_generator.noise2(x/flatness, y/flatness) + 1)/2) * (maximum - minimum) + minimum)
        for y in range(size[1]-1)
    ]
    for x in range(size[0]-1)
]

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